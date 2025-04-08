//document.querySelectorAll('input[name="work_experience_certificate"]').forEach((elem) => {
//    elem.addEventListener("change", function () {
//        document.getElementById("reasonField").style.display = (this.value === "No") ? "block" : "none";
//    });
//});


document.querySelectorAll('input[type="radio"]').forEach((elem) => {
        elem.addEventListener("change", function () {
            let fieldId = this.getAttribute("data-toggle-field");
            if (fieldId) {
                document.getElementById(fieldId).style.display = (this.value === "No") ? "block" : "none";
            }
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

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("myForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        let form = this;
        let formData = new FormData(form);

        // Show loading animation
        Swal.fire({
            title: "Processing...",
            text: "Please wait while we update the file.",
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        fetch("/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            Swal.close(); // Close loading animation

            if (data.message) {
                Swal.fire({
                    title: "Choose an Option",
                    text: "Do you want to print the document?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonText: "Print Now",
                    cancelButtonText: "Don't Print"
                }).then((result) => {
                    if (result.isConfirmed) {
                        // If "Print Now" is clicked, download the file
                        window.location.href = "/download";

                        // 🧹 Clear the form fields & scroll to top
                        setTimeout(() => {
                            form.reset();
                            window.scrollTo({ top: 0, behavior: "smooth" }); // 👈 Smooth scroll to top
                        }, 500);
                    } else {
                        // User chose "Don't Print", keep the form data
                        Swal.fire("You can continue editing!", "", "info");
                    }
                });
            } else if (data.error) {
                Swal.fire({
                    title: "Error!",
                    text: data.error,
                    icon: "error"
                });
            } else {
                throw new Error("Unexpected response format");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.close();
            Swal.fire("Error!", "Something went wrong. Check console for details.", "error");
        });
    });
});
