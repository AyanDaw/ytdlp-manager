"""
This file is the starting/entry point of the app.
"""

from modules import ui
# import time
import database
import shutil

def check_dependencies():
    missing = []
    if shutil.which('deno') is None:
        missing.append('Deno')
    if shutil.which('ffmpeg') is None:
        missing.append('ffmpeg')
    
    if missing:
        print(f"Warning: Missing recommended tools: {', '.join(missing)}")
        print("Some features may not work correctly.")
        print("Deno: https://deno.land")
        print("ffmpeg: https://ffmpeg.org")
        input("Press Enter to continue anyway...")

def main():
    database.initialize_db()
    check_dependencies()
    ui.splash()
    while True:
        action = ui.home()
        if action == "login":
            user = ui.login_ask() # Gets the current user and mode of user. Logged user or Guest. (username, mode)
            if user == None:
                input("Press \'Enter\' to return to HOME...")
                continue
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

# TODO: Ask User for cookies if YT-DLP doesnot work.