# YTDLP-MANAGER

A terminal-based personal download manager built around `yt-dlp`, with user accounts, bucket list, history tracking, and portable data.
---
[![Last Commit](https://img.shields.io/github/last-commit/AyanDaw/ytdlp-manager)]()
---

## What This Is

YTDLP-MANAGER is not just a downloader wrapper. It is a stateful CLI application with a full user system, persistent storage, and a screen-based interface — designed to feel like a real application, not a script.

---

## Features

- **User Accounts** — Register, login, or use as a guest
- **Download Engine** — Video, audio, and playlist downloads via yt-dlp
- **Bucket List** — Save links to download later, batch download anytime
- **History** — Track everything you've downloaded, tied to your account
- **Settings** — Per-user preferences (format, output folder)
- **Data Portability** — Export and import your data as JSON

---

## Project Structure

```
ytdlp-manager/
│
├── main.py               # Entry point — run this file
├── database.py           # All SQLite operations live here
│
├── data/
│   └── database.db       # Auto-generated on first run
│
└── modules/
    ├── __init__.py
    ├── ui.py             # All screens and user flow
    ├── auth.py           # Login, register, guest logic
    ├── display.py        # Reusable visual components
    ├── downloader.py     # yt-dlp wrapper
    ├── bucket.py         # Bucket list logic
    ├── history.py        # History tracking logic
    └── settings.py       # User preferences logic
```

---

## Architecture

The app follows a strict three-layer architecture. Each layer only talks to the one below it.

```
ui.py  →  auth / bucket / history / settings  →  database.py
```

- **UI layer** — handles all input and output, never touches the database directly
- **Logic layer** — processes data, enforces rules, talks to the database
- **Database layer** — the only file allowed to run SQL queries

---

## App Flow

```
Splash Screen
     ↓
Login Page  →  Register  →  back to Login
             →  Login
             →  Guest
     ↓
Main Menu
     ↓
Download / Bucket List / History / Settings / Exit
```

---

## Database Schema

All data lives in a single `database.db` file with four tables:

| Table | Purpose |
|---|---|
| `users_table` | User accounts |
| `bucket_list` | Saved links per user |
| `history` | Download history per user |
| `settings` | Per-user preferences |

Guest users have no database footprint.

---

## Data Portability

User data can be exported to a JSON file and imported back on any device. This is the intended way to transfer your account between machines.

> Export and Import features are planned for the Settings menu.

---

## Requirements

- Python 3.10+ (for `match/case` syntax)
- `yt-dlp` installed and accessible in PATH
<!-- 
Install yt-dlp:
```
pip install yt-dlp
``` -->

---

## Running the App

Always run through `main.py` from the project root:

```
python main.py
```

Never run individual module files directly in production — they are designed to be imported, not executed standalone.

---

## Security Notes

- Passwords are hashed using `SHA-256` before storage — plain text passwords are never saved
- SQL queries use parameterized statements to prevent SQL injection
- Guest mode leaves no data in the database

---

## Status

Currently in active development. Features being built in this order:

- [x] Project structure
- [x] Splash screen
- [x] Database initialization
- [x] User registration
- [x] User login
- [x] Guest mode
- [x] Main menu routing
- [ ] Main menus
- [ ] Download engine
- [ ] Bucket list
- [ ] History
- [ ] Settings
- [ ] Export / Import

---

