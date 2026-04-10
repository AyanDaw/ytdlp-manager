"""
This file is the starting/entry point of the app.
"""

from modules import ui
# import time
import database

def main():
    database.initialize_db()
    ui.splash()
    while True:
        action = ui.home()
        if action == "login":
            user = ui.login_ask() # Gets the current user and mode of user. Logged user or Guest. (username, mode)
            ui.menu(user=user) 
            user = None
            print("Logout successfull!")
            input("Press \'Enter\' to return to HOME...")
        elif action == "porter":
            pass  # build later
        elif action == "updater":
            pass  # build later
    
if __name__ == "__main__":
    main()