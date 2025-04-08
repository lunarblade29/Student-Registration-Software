from flask import Blueprint, render_template, request, send_file
import pandas as pd

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    df = pd.read_excel("students.xlsx")
    columns = df.columns.tolist()
    selected_columns = request.form.getlist("columns")
    filtered_data = df[selected_columns] if selected_columns else None
    return render_template(
        "dashboard.html",
        columns=columns,
        selected=selected_columns,
        data=filtered_data.to_dict(orient="records") if filtered_data is not None else None
    )


@dashboard_bp.route("/download", methods=["POST"])
def download():
    df = pd.read_excel("students.xlsx")  # <-- freshly reload the file
    selected_columns = request.form.getlist("columns")
    filtered_df = df[selected_columns] if selected_columns else df
    file_path = "filtered_data.xlsx"
    filtered_df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)
