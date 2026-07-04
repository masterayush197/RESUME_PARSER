from flask import Flask, render_template, request, redirect
import os
import pandas as pd
from flask import send_file

from parser import extract_resume_data
from database import *

app = Flask(__name__)

# -----------------------------
# Upload Folder Configuration
# -----------------------------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create SQLite database
create_database()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Upload Resume
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No file selected."

    file = request.files["resume"]

    if file.filename == "":
        return "Please choose a PDF."

    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Extract Resume Information
    data = extract_resume_data(filepath)

    # Save into SQLite
    save_resume(
        data["name"],
        data["email"],
        data["phone"],
        data["skills"],
        data["education"]
    )

    return render_template(
        "result.html",
        data=data
    )


# -----------------------------
# Resume History
# -----------------------------
@app.route("/history")
def history():

    resumes = get_all_resumes()

    total = total_resumes()

    return render_template(
        "history.html",
        resumes=resumes,
        total=total
    )


# -----------------------------
# Search Resume
# -----------------------------
@app.route("/search", methods=["POST"])
def search():

    keyword = request.form["keyword"]

    resumes = search_resume(keyword)

    return render_template(
        "history.html",
        resumes=resumes
    )


# -----------------------------
# Delete Resume
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):

    delete_resume(id)

    return redirect("/history")
# -----------------------------
# Run Application
# -----------------------------

@app.route("/export")
def export():

    data = get_resume_dataframe()

    df = pd.DataFrame(

        data,

        columns=[
            "ID",
            "Name",
            "Email",
            "Phone",
            "Skills",
            "Education"
        ]

    )

    filename = "Resume_Data.csv"

    df.to_csv(filename, index=False)

    return send_file(
        filename,
        as_attachment=True
    )

# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)