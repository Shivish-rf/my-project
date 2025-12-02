from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# Load quiz questions
with open("questions.json", "r") as f:
    questions = json.load(f)

# Create database if not exists
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/get_questions")
def get_questions():
    return jsonify(questions)

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.get_json()
    username = data["username"]
    score = data["score"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO leaderboard(username, score, date) VALUES (?, ?, ?)",
                (username, score, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Score saved"})

@app.route("/leaderboard")
def leaderboard():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT username, score, date FROM leaderboard ORDER BY score DESC LIMIT 10")
    records = cur.fetchall()
    conn.close()
    return render_template("leaderboard.html", records=records)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
