from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super-secret-key-ChangeThis123"

DATA_FILE = "data/students.json"

# Ensure data folder & file exist
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_students():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

def calculate_grade(avg):
    if avg >= 90: return "A+"
    elif avg >= 80: return "A"
    elif avg >= 70: return "B"
    elif avg >= 60: return "C"
    elif avg >= 50: return "D"
    else: return "F"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_student():
    try:
        roll = request.form.get("roll")
        name = request.form.get("name").strip()
        maths = float(request.form.get("maths"))
        physics = float(request.form.get("physics"))
        chemistry = float(request.form.get("chemistry"))

        # Input validation
        if not roll or not name:
            flash("Roll number and name are required!", "error")
            return redirect(url_for("index"))

        if not roll.isdigit() or int(roll) <= 0:
            flash("Roll number must be a positive integer!", "error")
            return redirect(url_for("index"))

        for m in [maths, physics, chemistry]:
            if not 0 <= m <= 100:
                flash("Marks must be between 0 and 100!", "error")
                return redirect(url_for("index"))

        students = load_students()

        # Check duplicate roll number
        if any(s["roll"] == roll for s in students):
            flash("Roll number already exists!", "error")
            return redirect(url_for("index"))

        total = maths + physics + chemistry
        avg = total / 3
        grade = calculate_grade(avg)

        student = {
            "roll": roll,
            "name": name,
            "maths": maths,
            "physics": physics,
            "chemistry": chemistry,
            "total": total,
            "average": round(avg, 2),
            "grade": grade,
            "added": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        students.append(student)
        save_students(students)

        flash("Student record added successfully!", "success")
        return redirect(url_for("index"))

    except ValueError:
        flash("Invalid marks! Please enter numeric values.", "error")
        return redirect(url_for("index"))

@app.route("/api/students")
def api_students():
    students = load_students()
    search = request.args.get("search", "").strip()

    if search:
        students = [s for s in students if search.lower() in s["roll"].lower()]

    return jsonify(students)

@app.route("/statistics")
def statistics():
    students = load_students()
    if not students:
        stats = {"highest": 0, "lowest": 0, "average": 0, "count": 0}
    else:
        totals = [s["total"] for s in students]
        stats = {
            "highest": max(totals),
            "lowest": min(totals),
            "average": round(sum(totals) / len(totals), 2),
            "count": len(students)
        }

    return render_template("statistics.html", stats=stats, students=students)

if __name__ == "__main__":
    app.run(debug=True)