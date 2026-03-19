document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const tbody = document.getElementById("studentsBody");

  function loadStudents(search = "") {
    fetch(`/api/students?search=${encodeURIComponent(search)}`)
      .then(res => res.json())
      .then(data => {
        tbody.innerHTML = "";

        if (data.length === 0) {
          tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;padding:2rem;">No records found</td></tr>`;
          return;
        }

        data.forEach(s => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${s.roll}</td>
            <td>${s.name}</td>
            <td>${s.maths}</td>
            <td>${s.physics}</td>
            <td>${s.chemistry}</td>
            <td>${s.total}</td>
            <td>${s.average}</td>
            <td class="grade-${s.grade.toLowerCase()}">${s.grade}</td>
            <td>${s.added}</td>
          `;
          tbody.appendChild(row);
        });
      })
      .catch(err => console.error("Error loading students:", err));
  }

  // Initial load
  loadStudents();

  // Live search
  let timeout;
  searchInput.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      loadStudents(searchInput.value.trim());
    }, 350);
  });
});