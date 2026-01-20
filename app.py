import os
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

UPLOAD_FOLDER = 'storage'
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = """
        SELECT * FROM Files
    """
    cursor.execute(sql)
    files = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("index.html", files=files)

@app.route('/file/<file_id>')
def file(file_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = """
        SELECT * FROM Files WHERE id = ?
    """
    cursor.execute(sql, (file_id,))
    file = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("file.html", file=file)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        file = request.files['file']
        if file:
            filename, ext = os.path.splitext(file.filename)
            filename = f"{uuid.uuid4()}{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, filename)) 
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            sql = """
                INSERT INTO Files (name, description, filename) VALUES (?, ?, ?)
            """
            cursor.execute(sql,(name, description, filename))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
    return render_template("upload.html")

init_db()
