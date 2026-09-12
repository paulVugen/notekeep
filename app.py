import sqlite3
import time
from pathlib import Path

from flask import Flask, g, jsonify, request

DB = Path("notes.db")
app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id INTEGER PRIMARY KEY, title TEXT NOT NULL, "
            "body TEXT DEFAULT '', created REAL)")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def row_to_dict(r):
    return {"id": r["id"], "title": r["title"],
            "body": r["body"], "created": r["created"]}


@app.get("/notes")
def list_notes():
    rows = get_db().execute(
        "SELECT * FROM notes ORDER BY id DESC LIMIT 100").fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@app.post("/notes")
def create_note():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO notes (title, body, created) VALUES (?, ?, ?)",
        (title, data.get("body", ""), time.time()))
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id = ?",
                     (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    db = get_db()
    cur = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "not found"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
