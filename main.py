from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Excel file path
EXCEL_FILE = "students.xlsx"

# Ensure the Excel file exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=[
        "Name", "Registration Number", "Biometric Verification Completed", "Gender",
        "Recent Photographs Submitted", "Marksheet X Verification", "Marksheet XII Verification",
        "Duration of Degree Course", "Degree Marksheet Verification", "Degree Certificate Verification",
        "Provisional Degree Certificate", "Graduation Marks Eligibility", "Graduation Status",
        "Incomplete Graduation Certificate", "Graduation Area", "Work Experience Certificate Submitted",
        "Work Experience Reason", "SC/ST/OBC/PwD Certificate Verification", "PwD Enclosure Submitted",
        "Demand Draft Submitted", "Demand Draft Amount", "Draft No.", "DT No.",
        "CAT Score Card Verification", "Guardian's Declaration Submitted", "Medical Info Form Submitted",
        "Personal Data Card Submitted", "Campus Rules Declaration Submitted", "Anti-Ragging Form Submitted",
        "Bank Details Declaration Submitted", "Bank Loan Taken", "Bank Name", "Loan Amount"
    ])
    df.to_excel(EXCEL_FILE, index=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect form data
        student_data = {
            "Name": request.form.get("name"),
            "Registration Number": request.form.get("reg_no"),
            "Biometric Verification Completed": request.form.get("biometric"),
            "Gender": request.form.get("gender"),
            "Recent Photographs Submitted": request.form.get("photos"),
            "Marksheet X Verification": request.form.get("marksheet_x"),
            "Marksheet XII Verification": request.form.get("marksheet_xii"),
            "Duration of Degree Course": request.form.get("degree_duration"),
            "Degree Marksheet Verification": request.form.get("degree_marksheet"),
            "Degree Certificate Verification": request.form.get("degree_certificate"),
            "Provisional Degree Certificate": request.form.get("provisional_degree"),
            "Graduation Marks Eligibility": request.form.get("marks_obtained"),
            "Graduation Status": request.form.get("graduation_status"),
            "Incomplete Graduation Certificate": request.form.get("incomplete_graduation_cert"),
            "Graduation Area": request.form.get("graduation_area"),
            "Work Experience Certificate Submitted": request.form.get("work_experience_certificate"),
            "Work Experience Reason": request.form.get("reason_for_no"),
            "SC/ST/OBC/PwD Certificate Verification": request.form.get("category_certificate"),
            "PwD Enclosure Submitted": request.form.get("pwd_enclosure"),
            "Demand Draft Submitted": request.form.get("demand_draft_submitted"),
            "Demand Draft Amount": request.form.get("demand_draft_amount") if request.form.get("demand_draft_submitted") == "Yes" else None,
            "Draft No.": request.form.get("draft_no") if request.form.get("demand_draft_submitted") == "Yes" else None,
            "DT No.": request.form.get("dt_no") if request.form.get("demand_draft_submitted") == "Yes" else None,
            "CAT Score Card Verification": request.form.get("cat_score_card"),
            "Guardian's Declaration Submitted": request.form.get("guardians_declaration"),
            "Medical Info Form Submitted": request.form.get("medical_info_form"),
            "Personal Data Card Submitted": request.form.get("personal_data_card"),
            "Campus Rules Declaration Submitted": request.form.get("campus_rules_declaration"),
            "Anti-Ragging Form Submitted": request.form.get("anti_ragging_form"),
            "Bank Details Declaration Submitted": request.form.get("bank_details_declaration"),
            "Bank Loan Taken": request.form.get("bank_loan"),
            "Bank Name": request.form.get("bank_name"),
            "Loan Amount": request.form.get("loan_amount")
        }

        # Append data to Excel
        df = pd.read_excel(EXCEL_FILE)
        df = df._append(student_data, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
