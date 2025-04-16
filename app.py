import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

UPLOAD_FOLDER = 'static/games'
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
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
        SELECT * FROM games
    """
    cursor.execute(sql)
    games = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("index.html", games=games)

@app.route('/game/<game_id>')
def game(game_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = """
        SELECT * FROM games WHERE id = ?
    """
    cursor.execute(sql, (game_id,))
    game = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("game.html", game=game)

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
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            sql = """
                INSERT INTO games (name, description, filename) VALUES (?, ?, ?)
            """
            cursor.execute(sql,(name, description, file.filename))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
    return render_template("upload.html")

init_db()
if __name__ == '__main__':
    app.run()
