import sqlite3

DATABASE = "resume.db"


# -----------------------------
# Create Database
# -----------------------------
def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            email TEXT,

            phone TEXT,

            skills TEXT,

            education TEXT

        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Save Resume
# -----------------------------
def save_resume(name, email, phone, skills, education):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO resumes
        (name, email, phone, skills, education)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            email,
            phone,
            ", ".join(skills),
            ", ".join(education)
        )
    )

    conn.commit()
    conn.close()


# -----------------------------
# Get All Resumes
# -----------------------------
def get_all_resumes():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resumes
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# -----------------------------
# Delete Resume
# -----------------------------
def delete_resume(resume_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM resumes WHERE id=?",
        (resume_id,)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Search Resume
# -----------------------------
def search_resume(keyword):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM resumes
        WHERE name LIKE ?
        OR skills LIKE ?
        """,
        (
            "%" + keyword + "%",
            "%" + keyword + "%"
        )
    )

    data = cursor.fetchall()

    conn.close()

    return data

def total_resumes():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM resumes")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_resume_dataframe():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resumes")

    data = cursor.fetchall()

    conn.close()

    return data