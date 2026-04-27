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

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS profiles(
                    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                    user_id         INTEGER     NOT NULL,
                    name            TEXT        NOT NULL,
                    format          TEXT        NOT NULL,
                    merge_format    TEXT        DEFAULT 'mp4'
                )
            """
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS queue(
                    id              INTEGER     PRIMARY KEY AUTOINCREMENT,
                    user_id         INTEGER     NOT NULL,
                    url             TEXT        NOT NULL,
                    profile_id      INTEGER,
                    position        INTEGER     NOT NULL,
                    status          TEXT        DEFAULT 'pending'
                )
            """
        )
        
        db.commit()


# ____________used by auth.py__________________________

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
            return (True, "Registration Successful!")
    except sqlite3.IntegrityError:
        return (False, "Username already taken")
    except Exception as e:
        return (False, f"Something went wrong: {e}")
    

# ____________used by ui.py for PRESETS______________________
def get_profiles(username: str) -> dict:
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT profiles.*
            FROM profiles
            JOIN users_table ON profiles.user_id = users_table.id
            WHERE users_table.username = ?
            """,
            (username,)
        )
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        """
            cursor.fetchall() returns a list of tuples and every tuple looks like this:
            (id, user_id, name, format, merge_format)
             0    1        2     3       4     
        
            After any cursor.execute(), SQLite stores metadata about the columns in cursor.description. It looks like this:
            cursor.description = (
                ('id', None, None, None, None, None, None),
                ('user_id', None, None, None, None, None, None),
                ('name', None, None, None, None, None, None),
                ('format', None, None, None, None, None, None),
                ('merge_format', None, None, None, None, None, None),
            )

            Each tuple's first element [0] is the column name. So:
            columns = [desc[0] for desc in cursor.description]
            # Result: ['id', 'user_id', 'name', 'format', 'merge_format']
    
            dict(zip(columns, row)) = {
                'id': 1,
                'user_id': 1,
                'name': 'My Preset',
                'format': 'bestvideo+bestaudio/best',
                'merge_format': 'mp4'
            }
            # Gives the dict format
        """

        profiles = {}
        for row in rows:
            row_dict = dict(zip(columns, row))
            profiles[row_dict['name']] = row_dict
        return profiles


def get_settings_data(username):
    # TODO: fetch from settings when settings module is built
    user_setting = None
    return None # For now
    ...

if __name__ == "__main__":
    initialize_db()