"""
This file is responsible for one thing only — talking to SQLite. Every other
 module that needs data goes through this file. Nothing else touches the 
database directly.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'data' / 'database.db'

def initialize_db():

    with sqlite3.connect(DB_PATH) as db: 
    # Connects or create database file.
    # No need of close() as with block automatically does it

        cursor = db.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS users_table(
                
                    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                    username        TEXT        UNIQUE NOT NULL,
                    password        TEXT        NOT NULL,
                    created_at      TEXT        DEFAULT CURRENT_TIMESTAMP
                
                )
            """
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS bucket_list(
                
                    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                    user_id         INTEGER     NOT NULL,
                    url             TEXT        NOT NULL,
                    title           TEXT        NOT NULL,
                    added_at        TEXT        DEFAULT CURRENT_TIMESTAMP

                )
            """
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS history(
                
                    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                    user_id         INTEGER     NOT NULL,
                    url             TEXT        NOT NULL,
                    format          TEXT        NOT NULL,
                    downloaded_at   TEXT        DEFAULT CURRENT_TIMESTAMP

                )
            """
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS settings(
                
                    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                    user_id         INTEGER     UNIQUE NOT NULL,
                    download_folder TEXT,
                    format          TEXT        DEFAULT 'mp4'

                )
            """
        )

        db.commit()

def get_user(username: str):
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users_table WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result
    # I am making it reusable for login so login can fetch data too. register will fetch
    # data in its end if it becomes true then register will throw error

def verify_user(username, hashed_password) -> bool:
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users_table WHERE username = ? AND password = ?", (username, hashed_password))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

def create_user(username, hashed_password):
    try:
        with sqlite3.connect(DB_PATH) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users_table (username, password) VALUES (?, ?)", (username, hashed_password,))
            db.commit()
            return "Registration Successful!"
    except sqlite3.IntegrityError:
        return "Username already taken"
    except Exception as e:
        return f"Something went wrong: {e}"

if __name__ == "__main__":
    initialize_db()