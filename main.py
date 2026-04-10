"""
This file is the starting/entry point of the app.
"""

from modules import ui
# import time
import database

def main():
    database.initialize_db()
    ui.splash()
    ui.home()
    user = ui.login_ask() # Gets the current user and mode of user. Logged user or Guest. (username, mode)
    ui.menu(user= user)
    
if __name__ == "__main__":
    main()