import sqlite3
from datetime import datetime

class FeedbackManager:
    def __init__(self, db_path="feedback.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT,
                query TEXT,
                response TEXT,
                rating INTEGER, -- 1 for Up, -1 for Down
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def record_feedback(self, thread_id, query, response, rating):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (thread_id, query, response, rating, timestamp) VALUES (?, ?, ?, ?, ?)",
            (thread_id, query, response, rating, datetime.now())
        )
        conn.commit()
        conn.close()
        print(f"Feedback recorded: {rating} for thread {thread_id}")

    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT rating, COUNT(*) FROM feedback GROUP BY rating")
        stats = cursor.fetchall()
        conn.close()
        return stats
