document.querySelectorAll('input[name="work_experience_certificate"]').forEach((elem) => {
    elem.addEventListener("change", function () {
        document.getElementById("reasonField").style.display = (this.value === "No") ? "block" : "none";
    });
});

document.querySelectorAll('input[name="bank_loan"]').forEach((elem) => {
    elem.addEventListener("change", function () {
        document.getElementById("loanDetails").style.display = this.value === "Yes" ? "block" : "none";
    });
});

    function toggleDDFields() {
        var ddSubmitted = document.querySelector('input[name="demand_draft_submitted"]:checked').value;
        var ddAmountDiv = document.getElementById("ddAmountDiv");
        var ddDetailsDiv = document.getElementById("ddDetailsDiv");

        if (ddSubmitted === "Yes") {
            ddAmountDiv.style.display = "block";
            ddDetailsDiv.style.display = "block";
        } else {
            ddAmountDiv.style.display = "none";
            ddDetailsDiv.style.display = "none";
        }
    }