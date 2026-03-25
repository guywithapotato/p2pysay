from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("MESSAGES_DB_PATH", str(BASE_DIR / "messages.db")))

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def fetch_recent_messages(limit: int = 50) -> list[dict[str, Any]]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, sender, body, created_at
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in reversed(rows)]


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/basic")
def basic_view() -> str:
    messages = fetch_recent_messages(100)
    return render_template("basic.html", messages=messages)


@app.post("/basic/send")
def basic_send() -> Any:
    sender = (request.form.get("sender") or "").strip()[:40]
    body = (request.form.get("body") or "").strip()[:1000]

    if sender and body:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO messages (sender, body) VALUES (?, ?)",
                (sender, body),
            )

    return redirect(url_for("basic_view"))


@app.get("/api/messages")
def list_messages() -> Any:
    limit = min(int(request.args.get("limit", 50)), 200)
    return jsonify(fetch_recent_messages(limit))


@app.post("/api/messages")
def send_message() -> Any:
    payload = request.get_json(silent=True) or {}
    sender = (payload.get("sender") or "").strip()[:40]
    body = (payload.get("body") or "").strip()[:1000]

    if not sender or not body:
        return jsonify({"error": "sender and body are required"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO messages (sender, body) VALUES (?, ?)",
            (sender, body),
        )
        message_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, sender, body, created_at FROM messages WHERE id = ?",
            (message_id,),
        ).fetchone()

    return jsonify(dict(row)), 201


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
