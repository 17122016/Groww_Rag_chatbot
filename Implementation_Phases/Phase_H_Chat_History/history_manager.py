import sqlite3
import json
from datetime import datetime

class ChatHistoryManager:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                role TEXT,
                content TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def add_message(self, thread_id, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (thread_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (thread_id, role, content, datetime.now())
        )
        conn.commit()
        conn.close()

    def get_history(self, thread_id, limit=5):
        """Fetches the last N exchanges for a specific thread."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Fetching last 'limit * 2' messages (pair of human/assistant)
        cursor.execute(
            "SELECT role, content FROM chat_history WHERE thread_id = ? ORDER BY timestamp DESC LIMIT ?",
            (thread_id, limit * 2)
        )
        history = cursor.fetchall()
        conn.close()
        
        # Reverse to get chronological order
        return history[::-1]

    def format_history_for_llm(self, thread_id, limit=5):
        history = self.get_history(thread_id, limit)
        formatted = ""
        for role, content in history:
            prefix = "Human" if role == "user" else "Assistant"
            formatted += f"{prefix}: {content}\n"
        return formatted
