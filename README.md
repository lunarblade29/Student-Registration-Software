# 🎓 Student Registration Software

Welcome to the **Student Registration Dashboard**, a powerful yet lightweight web application built with **Flask** that streamlines student data registration, analysis, and report generation.

---

## 🚀 Features

✅ **Student Registration Form**  
✅ **Dashboard View** with Filtering & Sorting  
✅ **Dynamic Column Selection**  
✅ **Excel Report Generation**  
✅ **Responsive UI with Bootstrap 5**  
✅ **Search Functionality**  
✅ **Interactive Data Table with Hover & Sorting**  
✅ **Custom Theming & Styling**  

---

## 🗂️ Folder Structure

```
Student-Registration-Software/
│
├── my_dashboard/
│   └── dashboard.py           # Main Flask route for the dashboard
│
├── static/                    # Static files (CSS, JS, images)
│   ├── script.js
│   ├── script2.js
│   ├── style.css
│   ├── style2.css
│   ├── dashboard.png
│   └── student_reg.png
│
├── templates/                 # HTML Templates
│   ├── index.html             # Main registration form
│   └── dashboard.html         # Dashboard view
│
├── uploads/                   # Uploaded/Generated Excel files
│   ├── students.xlsx
│   └── filtered_data.xlsx
│
├── downloads/
│   └── output.docx            # Exported documents (optional)
│
├── main.py                    # Main application entry point
├── README.md                  # You're reading it! 😊
└── .venv/                     # Virtual environment (not pushed to Git)
```

---

## 🖥️ How It Works

1. 📝 Students fill out the **registration form** (`index.html`).
2. 📊 Admin can **view and filter** the data in a **dashboard** (`dashboard.html`).
3. 📥 Choose any combination of columns and **generate downloadable Excel reports**.
4. 🔍 Use the **search bar** to quickly find student entries.
5. 🧾 Exported Excel reports are stored in `/uploads`.

---

## 🎨 UI Highlights

- **Bootstrap 5** based styling for responsive design.
- Custom **maroon buttons**, **hoverable tables**, and elegant **dark headers**.
- Uses **Bootstrap Select** for searchable dropdowns.
- Interactive sorting on table headers with visual arrow indicators.

---

## 📦 Setup Instructions

> 🐍 Python 3.8+ recommended

### 1️⃣ Create & Activate Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

### 2️⃣ Install Dependencies
```bash
pip install flask openpyxl pandas
```

### 3️⃣ Run the App
```bash
python main.py
```

Then, open your browser and visit:  
👉 `http://127.0.0.1:5000`

---

## 📄 Dependencies

- **Flask** - Web framework
- **Pandas** - For Excel processing
- **Openpyxl** - Excel export
- **Bootstrap 5** - UI Framework
- **Bootstrap Select** - For enhanced dropdowns

---

## 📌 Future Enhancements

- 🧾 PDF report export  
- 🔐 Authentication system  
- 📈 Charts & Analytics  
- ☁️ Cloud storage integration

---

## 🙌 Contribution

Have ideas or improvements?  
Feel free to fork and contribute via PRs! Let’s make student data handling easier, together.

---

## 🧑‍💻 Author

**Sanjiv Jadhav**  
Student @ IIMC | Explorer of Tech, Design & Possibility 🌍  
*“Approach every opportunity with humility and curiosity.”*

---

## 📝 License

This project is licensed under the MIT License.
```

---

Let me know if you want a version with badges (like build status, Python version, etc.) or a minimal TL;DR version for quicker overview!