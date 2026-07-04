import pdfplumber
import re


import pdfplumber
import re

SKILLS = [
    "Python", "Java", "C", "C++", "JavaScript",
    "HTML", "CSS", "SQL", "Flask",
    "Django", "Machine Learning", "AI",
    "Data Science", "React", "Node.js",
    "Git", "GitHub", "MongoDB", "MySQL"
]

EDUCATION = [
    "B.Tech",
    "B.E",
    "M.Tech",
    "MCA",
    "BCA",
    "B.Sc",
    "M.Sc",
    "MBA",
    "Diploma"
]


def extract_resume_data(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # Email
    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    email = email[0] if email else "Not Found"

    # Phone
    phone = re.findall(
        r"\+?\d[\d\s-]{8,}\d",
        text
    )

    phone = phone[0] if phone else "Not Found"

    # Name
    name = "Not Found"

    for line in text.split("\n"):

        line = line.strip()

        if len(line) > 2:

            name = line

            break

    # Skills
    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    # Education
    found_education = []

    for edu in EDUCATION:

        if edu.lower() in text.lower():
            found_education.append(edu)

    return {

        "name": name,

        "email": email,

        "phone": phone,

        "skills": found_skills,

        "education": found_education,

        "text": text

    }