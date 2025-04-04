from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
import os
from docx import Document  # Import python-docx

app = Flask(__name__)

# Excel file path
EXCEL_FILE = "students.xlsx"
TEMPLATE_PATH = "templates/template.docx"  # Path to the Word template

today_date = datetime.today().strftime('%d %B %Y')

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
        "Bank Details Declaration Submitted", "Bank Loan Taken", "Bank Name", "Loan Amount", "Remarks"
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
            "Loan Amount": request.form.get("loan_amount"),
            "Remarks": request.form.get("remarks"),
        }

        # Append data to Excel
        df = pd.read_excel(EXCEL_FILE)
        df = df._append(student_data, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        # 2. Update the Word Document
        # Load template and replace placeholders with form data
        doc = Document("templates/template.docx")  # Make sure the correct path is used

        for paragraph in doc.paragraphs:
            if "{name}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{name}", student_data["Name"])
            if "{reg_no}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{reg_no}", student_data["Registration Number"])
            if "{year}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{year}", student_data["Duration of Degree Course"])
            if "{grad_status}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{grad_status}", student_data["Graduation Status"])
            if "{resign}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{resign}", student_data["Work Experience Reason"])
            if "{bank_name}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{bank_name}", student_data["Bank Name"])
            if "{bank_amount}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{bank_amount}", student_data["Loan Amount"])
            if "{date}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{date}", today_date)
            if "{remarks}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{remarks}", student_data["Remarks"])

            # Handling the genders
            if "{gm}" in paragraph.text:
                if student_data["Gender"] == "Male":
                    paragraph.text = paragraph.text.replace("{gm}", "☑")  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{gf}", "☐")  # blank for No
                    paragraph.text = paragraph.text.replace("{go}", "☐")  # blank for No
                elif student_data["Gender"] == "Female":
                    paragraph.text = paragraph.text.replace("{gm}", "☐")  # blank for Yes
                    paragraph.text = paragraph.text.replace("{gf}", "☑")  # Tick for N
                    paragraph.text = paragraph.text.replace("{go}", "☐")  # blank for No
                else:
                    paragraph.text = paragraph.text.replace("{gm}", "☐")  # blank for Yes
                    paragraph.text = paragraph.text.replace("{gf}", "☐")  # Tick for N
                    paragraph.text = paragraph.text.replace("{go}", "☑")  # blank for No

            # Handling the drafts
            if "{dty}" in paragraph.text:
                if student_data["Demand Draft Amount"] == "440000":
                    paragraph.text = paragraph.text.replace("{dty}", "☑")  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dtn}", "☐")  # blank for No
                    paragraph.text = paragraph.text.replace("{ddt}", student_data["Draft No."])  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dtt}", student_data["DT No."])  # blank for No
                else:
                    paragraph.text = paragraph.text.replace("{dty}", "☐")  # blank for Yes
                    paragraph.text = paragraph.text.replace("{dtn}", "☑")  # Tick for N
                    paragraph.text = paragraph.text.replace("{ddt}", "------")  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dtt}", "------")  # blank for No
            if "{dcy}" in paragraph.text:
                if student_data["Demand Draft Amount"] == "20000":
                    paragraph.text = paragraph.text.replace("{dcy}", "☑")  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dcn}", "☐")  # blank for No
                    paragraph.text = paragraph.text.replace("{ddc}", student_data["Draft No."])  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dtc}", student_data["DT No."])  # blank for No
                else:
                    paragraph.text = paragraph.text.replace("{dcy}", "☐")  # blank for Yes
                    paragraph.text = paragraph.text.replace("{dcn}", "☑")  # Tick for N
                    paragraph.text = paragraph.text.replace("{ddc}", "------")  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dtc}", "------")  # blank for No
            if "{ddy}" in paragraph.text:
                if student_data["Demand Draft Amount"] == "460000":
                    paragraph.text = paragraph.text.replace("{ddy}", "☑")  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{ddn}", "☐")  # blank for No
                    paragraph.text = paragraph.text.replace("{ddb}", student_data["Draft No."])  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dtb}", student_data["DT No."])  # blank for No
                else:
                    paragraph.text = paragraph.text.replace("{ddy}", "☐")  # blank for Yes
                    paragraph.text = paragraph.text.replace("{ddn}", "☑")  # Tick for N
                    paragraph.text = paragraph.text.replace("{ddb}", "------")  # Tick for Yes
                    paragraph.text = paragraph.text.replace("{dtb}", "------")  # blank for No

            # Handling the streams
            if "{gse}" in paragraph.text and student_data["Graduation Area"] == "Engineering":
                paragraph.text = paragraph.text.replace("{gse}", "☑")  # Tick for Yes
                paragraph.text = paragraph.text.replace("{gss}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsc}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsa}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gso}", "☐")  # blank for No
            if "{gss}" in paragraph.text and student_data["Graduation Area"] == "Science":
                paragraph.text = paragraph.text.replace("{gss}", "☑")  # Tick for Yes
                paragraph.text = paragraph.text.replace("{gse}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsc}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsa}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gso}", "☐")  # blank for No
            if "{gsc}" in paragraph.text and student_data["Graduation Area"] == "Commerce":
                paragraph.text = paragraph.text.replace("{gsc}", "☑")  # Tick for Yes
                paragraph.text = paragraph.text.replace("{gss}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gse}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsa}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gso}", "☐")  # blank for No
            if "{gsa}" in paragraph.text and student_data["Graduation Area"] == "Arts":
                paragraph.text = paragraph.text.replace("{gsa}", "☑")  # Tick for Yes
                paragraph.text = paragraph.text.replace("{gss}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsc}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gse}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gso}", "☐")  # blank for No
            if "{gso}" in paragraph.text and student_data["Graduation Area"] == "Others":
                paragraph.text = paragraph.text.replace("{gso}", "☑")  # Tick for Yes
                paragraph.text = paragraph.text.replace("{gss}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsc}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gsa}", "☐")  # blank for No
                paragraph.text = paragraph.text.replace("{gse}", "☐")  # blank for No

        # Helper function to handle Yes/No placeholder replacement
        def handle_checkbox_placeholder(paragraph, placeholder_yes, placeholder_no, placeholder_na, student_data_value):
            if placeholder_yes in paragraph.text or placeholder_no in paragraph.text or placeholder_na in paragraph.text:
                if student_data_value == "Yes":
                    paragraph.text = paragraph.text.replace(placeholder_yes, "☑")  # Tick for Yes
                    paragraph.text = paragraph.text.replace(placeholder_no, "☐")  # blank for No
                    paragraph.text = paragraph.text.replace(placeholder_na, "☐")  # blank for NA
                elif student_data_value == "No":
                    paragraph.text = paragraph.text.replace(placeholder_yes, "☐")  # blank for Yes
                    paragraph.text = paragraph.text.replace(placeholder_no, "☑")  # Tick for No
                    paragraph.text = paragraph.text.replace(placeholder_na, "☐")  # blank for NA
                else:
                    paragraph.text = paragraph.text.replace(placeholder_yes, "☐")  # blank for Yes
                    paragraph.text = paragraph.text.replace(placeholder_no, "☐")  # blank for No
                    paragraph.text = paragraph.text.replace(placeholder_na, "☑")  # Tick for NA

        # Now use this helper function for all fields
        for paragraph in doc.paragraphs:
            handle_checkbox_placeholder(paragraph, "{by}", "{bn}", "{na}",
                                        student_data["Biometric Verification Completed"])
            handle_checkbox_placeholder(paragraph, "{py}", "{pn}", "{na}", student_data["Recent Photographs Submitted"])
            handle_checkbox_placeholder(paragraph, "{xy}", "{xn}", "{na}", student_data["Marksheet X Verification"])
            handle_checkbox_placeholder(paragraph, "{xiiy}", "{xiin}", "{na}",
                                        student_data["Marksheet XII Verification"])
            handle_checkbox_placeholder(paragraph, "{my}", "{mn}", "{na}",
                                        student_data["Degree Marksheet Verification"])
            handle_checkbox_placeholder(paragraph, "{cy}", "{cn}", "{na}",
                                        student_data["Degree Certificate Verification"])
            handle_checkbox_placeholder(paragraph, "{gy}", "{gn}", "{na}", student_data["Graduation Marks Eligibility"])
            handle_checkbox_placeholder(paragraph, "{csy}", "{csn}", "{na}",
                                        student_data["CAT Score Card Verification"])
            handle_checkbox_placeholder(paragraph, "{gdy}", "{gdn}", "{na}",
                                        student_data["Guardian's Declaration Submitted"])
            handle_checkbox_placeholder(paragraph, "{miy}", "{min}", "{na}",
                                        student_data["Medical Info Form Submitted"])
            handle_checkbox_placeholder(paragraph, "{pcy}", "{pcn}", "{na}",
                                        student_data["Personal Data Card Submitted"])
            handle_checkbox_placeholder(paragraph, "{cry}", "{crn}", "{na}",
                                        student_data["Campus Rules Declaration Submitted"])
            handle_checkbox_placeholder(paragraph, "{ary}", "{arn}", "{na}",
                                        student_data["Anti-Ragging Form Submitted"])
            handle_checkbox_placeholder(paragraph, "{bdy}", "{bdn}", "{na}",
                                        student_data["Bank Details Declaration Submitted"])
            handle_checkbox_placeholder(paragraph, "{loy}", "{lon}", "{na}", student_data["Bank Loan Taken"])
            # 3 fields
            handle_checkbox_placeholder(paragraph, "{pdy}", "{pdn}", "{pdna}",
                                        student_data["Provisional Degree Certificate"])
            handle_checkbox_placeholder(paragraph, "{igy}", "{ign}", "{igna}",
                                        student_data["Incomplete Graduation Certificate"])
            handle_checkbox_placeholder(paragraph, "{ry}", "{rn}", "{rna}",
                                        student_data["Work Experience Certificate Submitted"])
            handle_checkbox_placeholder(paragraph, "{ccy}", "{ccn}", "{ccna}",
                                        student_data["SC/ST/OBC/PwD Certificate Verification"])
            handle_checkbox_placeholder(paragraph, "{psy}", "{psn}", "{psna}", student_data["PwD Enclosure Submitted"])

        # Save the updated document
        output_path = os.path.join("downloads", "output.docx")
        doc.save(output_path)

        return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/download")
def download():
    return send_from_directory(directory="downloads", filename="output.docx")


if __name__ == "__main__":
    app.run(debug=True)
