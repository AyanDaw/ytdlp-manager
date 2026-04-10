import time
from modules import display, auth


def splash():
    display.clear_screen()
    display.display_logo()                                               
                                                                                   
    time.sleep(0.5)
    display.loading_animation(message = "Loading...", duration = 1)

    time.sleep(0.5)
    display.loading_animation(message = "Loading Modules...", duration = 2)

    time.sleep(0.5)
    input("Press \"Enter\" to continue.")
    return

def home():
    while True:
        display.clear_screen()
        display.display_logo()
        print("="*10, "HOME", "="*10)
        print("1. LOGIN - Move to Login Page!")
        print("2. PORTER - Import/Export your Data!")
        print("3. EXIT - Exit the app... :( ")

        try:
            option = int(input("Enter your option:> "))
        except ValueError:
            print("Please enter a number!")
            input()
            continue

        match option:
            case 1: 
                ...
            case 2:
                ...
            case 3:
                ...
            case _:
                print("Invalid option, try again")
                continue


def login_ask():
    while True:
        display.clear_screen()
        display.display_logo()
        # ask user to login / register / guest
        print("="*10, "LOGIN PAGE", "="*10)
        print("1. LOGIN - Log-in into your account!")
        print("2. REGISTER - Create a new user account!")
        print("3. GUEST - Use as a guest!")

        try:
            option = int(input("Enter your option:> "))
        except ValueError:
            print("Please enter a number!")
            input()
            continue
        match option:
            case 1: 
                current_user = login()
                return (current_user, "Logged User")
            case 2:
                result = register()
                print(result)
                input("Press \'ENTER\' to return to the \'LOGIN PAGE\'")
                continue
            case 3:
                current_user = guest()
                return (current_user, "Guest User")
            case _:
                print("Invalid option, try again")
                continue

def login():
    while True:
        display.clear_screen()
        display.display_logo()
        print("* LOGIN", "="*15)
        username = display.styled_input(prompt= "username")
        password = display.styled_input(prompt= "password")
        result = auth.login(username = username, password = password)
        if result:
            return username
        else:
            print("Entered Username or Password is wrong! Please Try Again!!")
            input("Press Enter to Try again!")
            continue

def register():
    while True:
        display.clear_screen()
        display.display_logo()
        print("* REGISTER A NEW USER", "="*15)
        username = display.styled_input(prompt= "username")
        if auth.check_username(username):
            print("Username already taken! Try a different username!")
            input("Press Enter to Try again!")
            continue
        else:
            password = display.styled_input(prompt= "password")
            result = auth.register(username = username, password = password)
        return result

def guest():
    display.loading_animation(message= "Please wait!... Logging in as a Guest...", duration= 2)
    return "GUEST"

def menu(user):
    if user[1] == "Logged User":
        menu_logged_user(user= user)
    elif user[1] == "Guest User":
        menu_guest(user= user)
    else:
        print("something went wrong!")

def menu_logged_user(user):    
    while True:
        display.clear_screen()
        display.display_logo()
        print(f"Hello! Welcome, {user[0]}")
        print("* MAIN MENU", "="*15)
        print("1. Download") # Takes to the download page
        print("2. Bucket List") # Creating, editing, marking done or viewing the list
        print("3. History") # Automatically Updates when user downloads something
        print("4. Settings") # Create or add new settings profile
        print("0. Logout") # Sends back to the Login page and Erases user

        try:
            option = int(input("Enter your option:> "))
        except ValueError:
            print("Please enter a number!")
            input()
            continue

        match option:
            case 1: 
                ...
            case 2:
                ...
            case 3:
                ...
            case _:
                print("Invalid option, try again")
                continue

def menu_guest(user):
    while True:
        display.clear_screen()
        display.display_logo()
        print(f"Hello! Welcome, {user[0]}")
        print("* MAIN MENU FOR GUEST", "="*15)
        print("1. Download") # Takes to the download page, anonomously
        print("0. Exit to Login") # Takes to Login (But confused how to do it cause it will make a stack of calls if i call login_ask() here as return)

        try:
            option = int(input("Enter your option:> "))
        except ValueError:
            print("Please enter a number!")
            input()
            continue

        match option:
            case 0: 
                ...
            case 1:
                ...
            case _:
                print("Invalid option, try again")
                continue

if __name__ == "__main__":
    splash()