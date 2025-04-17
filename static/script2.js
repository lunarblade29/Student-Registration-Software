// Sort function
function sortTable(columnIndex) {
    var table = document.getElementById("dataTable");
    var tbody = table.querySelector("tbody");
    var rows = Array.from(tbody.querySelectorAll("tr"));
    var ascending = table.getAttribute("data-sort-order") !== "asc";

    rows.sort((a, b) => {
        let cellA = a.cells[columnIndex].textContent.trim().toLowerCase();
        let cellB = b.cells[columnIndex].textContent.trim().toLowerCase();

        if (!isNaN(cellA) && !isNaN(cellB)) {
            return ascending ? cellA - cellB : cellB - cellA;
        } else {
            return ascending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
        }
    });

    table.setAttribute("data-sort-order", ascending ? "asc" : "desc");

    tbody.innerHTML = "";
    rows.forEach(row => tbody.appendChild(row));
}

// Search function
document.addEventListener("DOMContentLoaded", () => {
    let searchBox = document.getElementById("searchBox");
    if (searchBox) {
        searchBox.addEventListener("input", function () {
            let searchText = this.value.toLowerCase();
            let rows = document.querySelectorAll("#dataTable tbody tr");

            rows.forEach(row => {
                let rowText = row.innerText.toLowerCase();
                row.style.display = rowText.includes(searchText) ? "" : "none";
            });
        });
    }
});

$(document).ready(function () {
    $('.selectpicker').selectpicker();
});

function confirmClear() {
    const input = prompt("Type 'CLEAR' to confirm deletion of all data:");
    if (input === "CLEAR") {
        return true;  // allow form submission
    } else {
        alert("Action canceled. You must type 'CLEAR' exactly.");
        return false; // prevent form submission
    }
}