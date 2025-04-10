document.querySelectorAll('input[type="radio"]').forEach((elem) => {
  elem.addEventListener("change", function () {
    let fieldId = this.getAttribute("data-toggle-field");
    if (fieldId) {
      document.getElementById(fieldId).style.display =
        this.value === "No" ? "block" : "none";
    }
  });
});

document.querySelectorAll('input[name="bank_loan"]').forEach((elem) => {
  elem.addEventListener("change", function () {
    document.getElementById("loanDetails").style.display =
      this.value === "Yes" ? "block" : "none";
  });
});

function toggleDDFields() {
  var ddSubmitted = document.querySelector(
    'input[name="demand_draft_submitted"]:checked'
  ).value;
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
  document
    .getElementById("myForm")
    .addEventListener("submit", function (event) {
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
        },
      });

      fetch("/", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          Swal.close(); // Close loading animation

          if (data.message) {
            Swal.fire({
              title: "Choose an Option",
              text: "Do you want to print the document?",
              icon: "question",
              showCancelButton: true,
              confirmButtonText: "Print Now",
              cancelButtonText: "Don't Print",
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
              icon: "error",
            });
          } else {
            throw new Error("Unexpected response format");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          Swal.close();
          Swal.fire(
            "Error!",
            "Something went wrong. Check console for details.",
            "error"
          );
        });
    });
});

function fetchStudentInfo(regNo) {
  fetch("/get_student_info", {
    // Changed endpoint to /get_student_info
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "reg_no=" + encodeURIComponent(regNo),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("name").value = data.name;
      document.getElementById("email").value = data.email; // Populate the email field
    })
    .catch((error) => {
      console.error("Error fetching student info:", error); // Updated error message
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const regNoInput = document.getElementById("reg_no");
  regNoInput.addEventListener("input", function () {
    const currentRegNo = this.value.trim();
    if (currentRegNo) {
      fetchStudentInfo(currentRegNo); // Updated function call
    } else {
      document.getElementById("name").value = "";
      document.getElementById("email").value = ""; // Clear email as well
    }
  });
});

// JavaScript to handle the initial file upload
function handleInitialUpload() {
  const form = document.querySelector(
    'form[action="/upload_registration_data"]'
  );
  const formData = new FormData(form);

  fetch("/upload_registration_data", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        // Check if the response status is in the 2xx range
        if (response.status === 204) {
          Swal.fire({
            icon: "success",
            title: "File Ready",
            text: "File uploaded and ready for finalization.",
            timer: 2000,
            showConfirmButton: false,
          });
        } else {
          console.log("Initial upload response:", response); // Log unexpected success status
          Swal.fire({
            icon: "warning",
            title: "Upload Status",
            text: "File processed by server.", // Generic success message
          });
        }
      } else {
        console.error(
          "Initial upload error[][][]:",
          response.status,
          response.statusText
        );
        let errorMessage = "An error occurred during the initial upload.";
        if (response.status === 400) {
          errorMessage = "Invalid file or filename.";
        } else if (response.status === 415) {
          errorMessage = "Unsupported file type.";
        }
        Swal.fire({
          icon: "error",
          title: "Upload Error",
          text: errorMessage,
        });
      }
    })
    .catch((error) => {
      console.error("Error uploading file:", error);
      Swal.fire({
        icon: "error",
        title: "Upload Error",
        text: "An error occurred during the upload.",
      });
    });
}

// JavaScript for finalizing the upload
document
  .getElementById("finalizeUploadButton")
  .addEventListener("click", function () {
    fetch("/finalize_upload_registration_data", {
      method: "POST",
    })
      .then((response) => {
        if (response.ok) {
          if (response.status === 204) {
            Swal.fire({
              icon: "success",
              title: "Upload Successful",
              text: "Registration data file has been successfully replaced.",
            }).then(() => {
              // Reset the file input value
              document.getElementById("file").value = "";
            });
          } else {
            console.log("Finalize upload response:", response);
            Swal.fire({
              icon: "warning",
              title: "Upload Status",
              text: "File finalized on server.",
            }).then(() => {
              document.getElementById("file").value = "";
            });
          }
        } else {
          console.error(
            "Finalize upload error:",
            response.status,
            response.statusText
          );
          let errorMessage = "An error occurred while finalizing the upload.";
          if (response.status === 400) {
            errorMessage = "No file has been uploaded yet.";
          } else if (response.status === 500) {
            errorMessage =
              "An error occurred on the server while finalizing upload.";
          }
          Swal.fire({
            icon: "error",
            title: "Upload Error",
            text: errorMessage,
          });
        }
      })
      .catch((error) => {
        console.error("Error finalizing upload:", error);
        Swal.fire({
          icon: "error",
          title: "Upload Error",
          text: "An error occurred while finalizing the upload.",
        });
      });
  });
