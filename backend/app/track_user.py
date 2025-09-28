import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from app.config import *
import sqlite3

class TrackUser:
    def __init__(self):
        self.USER_DB = USER_INFO_PATH
    
    def init_db(self):
        conn = sqlite3.connect(self.USER_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            session_id TEXT,
            role TEXT,
            content TEXT
        )""")
        conn.commit()
        conn.close()
    
    def user_init_db(self):
        conn = sqlite3.connect(self.USER_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT UNIQUE,
            password TEXT
        )""")
        conn.commit()
        conn.close()
    
    def create_user(self, user_name, password):
        self.user_init_db()  # Ensure user table exists
        conn = sqlite3.connect(self.USER_DB)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (user_name, password) VALUES (?, ?)", (user_name, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def authenticate_user(self, user_name, password):
        conn = sqlite3.connect(self.USER_DB)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_name = ? AND password = ?", (user_name, password))
        user = c.fetchone()
        conn.close()
        return user is not None
    
    def add_message(self, user_name, session_id, role, content):
        self.init_db()  # Ensure messages table exists
        conn = sqlite3.connect(self.USER_DB)
        c = conn.cursor()
        c.execute("INSERT INTO messages (user_name, session_id, role, content) VALUES (?, ?, ?, ?)",
                  (user_name, session_id, role, content))
        conn.commit()
        conn.close()
    
    def get_messages(self, user_name, session_id):
        self.init_db()  # Ensure messages table exists
        conn = sqlite3.connect(self.USER_DB)
        c = conn.cursor()
        c.execute("SELECT role, content FROM messages WHERE user_name = ? AND session_id = ?",
                  (user_name, session_id))
        messages = c.fetchall()
        conn.close()
        return messages
    
    def get_sessions(self, user_name):
        self.init_db()  # Ensure messages table exists
        conn = sqlite3.connect(self.USER_DB)
        c = conn.cursor()
        c.execute("SELECT DISTINCT session_id FROM messages WHERE user_name = ?", (user_name,))
        sessions = [row[0] for row in c.fetchall()]
        conn.close()
        return sessions
    
    
    

