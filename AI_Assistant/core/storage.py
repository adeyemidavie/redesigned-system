import sqlite3
from pathlib import Path

# Create instance folder if it doesn't exist
Path("instance").mkdir(exist_ok=True)

DB_FILE = "instance/assistant.db"


def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(chat_id)
        REFERENCES chats(id)
        ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


def create_chat(title="New Chat"):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chats(title) VALUES(?)",
        (title,)
    )

    chat_id = cur.lastrowid

    conn.commit()
    conn.close()

    return chat_id


def get_chats():

    conn = connect()

    rows = conn.execute("""
        SELECT *
        FROM chats
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def rename_chat(chat_id, title):

    conn = connect()

    conn.execute(
        """
        UPDATE chats
        SET title=?
        WHERE id=?
        """,
        (title, chat_id)
    )

    conn.commit()
    conn.close()


def delete_chat(chat_id):

    conn = connect()

    conn.execute(
        "DELETE FROM chats WHERE id=?",
        (chat_id,)
    )

    conn.commit()
    conn.close()


def save_message(chat_id, role, content):

    conn = connect()

    conn.execute(
        """
        INSERT INTO messages(
            chat_id,
            role,
            content
        )
        VALUES(?,?,?)
        """,
        (
            chat_id,
            role,
            content
        )
    )

    conn.commit()
    conn.close()


def get_messages(chat_id):

    conn = connect()

    rows = conn.execute(
        """
        SELECT role, content
        FROM messages
        WHERE chat_id=?
        ORDER BY id
        """,
        (chat_id,)
    ).fetchall()

    conn.close()

    return [
        {
            "role": row["role"],
            "content": row["content"]
        }
        for row in rows
    ]