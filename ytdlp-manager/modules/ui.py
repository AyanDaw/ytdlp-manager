import time
from pathlib import Path
from modules import display, auth, downloader
from modules import custom_download_ui, quick_download_ui
import database
import sys

FILE_DIR = Path(__file__).parent # ytdlp-manager/modules
BASE_DIR = FILE_DIR.parent # ytdlp-manager

#___________HOME & SPLASH SCREENS______________________
# main() -> splash() -> main() -> home()
# Function Code Status: Complete Till Now
def splash():

    """
        This function does nothing than showing a landing page and Loading page.
        !Note: Loading Page loaders are fake for now
    """


    display.clear_screen()
    display.display_logo()                                                                                                                       
    time.sleep(0.5)
    display.loading_animation(message = "Loading...", duration = 1)
    time.sleep(0.5)
    display.loading_animation(message = "Loading Modules...", duration = 1)
    time.sleep(0.5)
    input("Press \"Enter\" to continue.")
    return


#                     (decision)
# main() -> home() -> Login -> \
#                  -> Porter -> \
#                  -> Updater ->/  main() -> /takes decision/
#                  -> Exit ->  /
# Function Code Status: Complete Till Now
def home():

    """
    This function doesnt call any functions, it just take the option inputted by the user
    and sends back this to main.py. there a while true loop handles the calling to avoid 
    call stack
    example: if a user keeps doing constantly login and logout, it makes a call stack that 
             might overload the system if home function calls the functions
             so the while loop resets the call stack every time.
    """


    while True:
        display.clear_screen()
        display.display_logo()
        title = "="*10+"HOME"+"="*10
        options = {
            '1': 'LOGIN - Move to Login Page!',
            '2': 'PORTER - Import/Export your Data!',
            '3': 'UPDATER - Will check for any available updates!',
            '0': 'EXIT - Exit the app... :( '
        }
        display.print_menu(title= title, options= options)
        try:
            option = int(input("Enter your option:> "))
        except ValueError:
            print("Please enter a number!")
            input()
            continue

        match option:
            case 0:
                # This is to exit the app.
                # Till now it seems done.
                display.clear_screen()
                display.display_logo()
                display.loading_animation(message= "Exiting...", duration= 1)
                print("\nHave a good day!... :)")
                sys.exit()
            
            case 1: 
                # This is for login_ask()
                # Sends to the main having while loop
                # Till now it seems done.
                display.loading_animation(message= "Moving to the login page...", duration= 1)
                return "login"
            
            case 2:
                # This is for Import/Export option
                # Sends to the main having while loop
                # Till now it seems done.
                # !Note: porter isnt done yet
                display.loading_animation(message= "Moving to the import/export page...", duration= 1)
                return "porter"
            case 3:
                # This is to Update the app
                # Sends to the main having while loop
                # Sends to the main having while loop
                # !Note: porter isnt done yet
                display.loading_animation(message= "Moving to the updater page...", duration= 1)
                return "updater"
            case _:
                # Fallback
                print("Invalid option, try again")
                continue



# _______ AUTH SCREENS_________________________________
#                                                                                                           (Returns User type)
# home() -> main(decision: Login) -> login_ask() /takes desion as input/ -> login() -> /returns to login_ask()/ Logged User    \
#                                                                        -> register() -> /returns to login_ask() to login/     >  main() -> menu() /menu takes its further decisions/
#                                                                        -> guest() -> /returns to login_ask()/ Guest User     / 
# Function Code Status: Complete Till Now
def login_ask():

    """
    This function takes the command after home page asks main to call it.
    This fn. is a decision maker function. It take decision what kind of user is going to this.
    If its a new user then it sends the user to register page, then login
    If old then sends to login directly
    If the user want to use the app without any login or registration then it 
    sends the user to guest. later it returns user-kind labels
    "Logged User" for the user who logged in
    "Guest User" for the user who entered as guest. 
    Guest will have some less features than logged user
    """


    while True:

        display.clear_screen()
        display.display_logo()
        title = "="*10+"LOGIN PAGE"+"="*10
        options = {
            '1': 'LOGIN - Log-in into your account!',
            '2': 'REGISTER - Create a new user account!',
            '3': 'GUEST - Use as a guest!',
            '0': 'Back'
        }
        display.print_menu(title= title, options= options)

        try:
            option = int(input("Enter your option:> "))
        except ValueError:
            print("Please enter a number!")
            input()
            continue

        match option:
            case 0:
                # Back
                return None
            case 1:
                # For Login 
                current_user = login()
                if(current_user == None):
                    return None
                return (current_user, "Logged User")
            case 2:
                # For Register
                result = register()
                if(result == None):
                    return None
                print(result[1])
                input("Press \'ENTER\' to return to the \'LOGIN PAGE\'")
                continue
            case 3:
                # For Guest
                current_user = guest()
                return (current_user, "Guest User")
            case _:
                # Fallback
                print("Invalid option, try again")
                continue

# -> login_ask(Decision: Login) /Does its authentication using auth/
# Function Code Status: Complete Till Now
def login():

    """
        Does its authentication using auth
        Uses while to reset wrong input
    """

    while True:
        display.clear_screen()
        display.display_logo()
        print("* LOGIN", "="*15)
        print("(To go back to the home screen type: 'ReturnLOGOUT' in username)\n")
        username = display.styled_input(prompt= "username")
        if(username == "ReturnLOGOUT"):
            return None
        password = display.styled_input(prompt= "password")
        result = auth.login(username = username, password = password)
        if result:
            return username
            # Returns the logged user to keep him remember
        else:
            print("Entered Username or Password is wrong! Please Try Again!!")
            input("Press Enter to Try again!")
            continue

# -> login_ask(Decision: Register) /Does its new user creation using auth/
# Function Code Status: Complete Till Now
def register():
    """
        This just registers a new user nothing related to authentication
        Uses while to reset common username input
        returns relay the result of creating a new user in database, either successful or not
    """
    while True:
        display.clear_screen()
        display.display_logo()
        print("* REGISTER A NEW USER", "="*15)
        print("(To go back to the home screen type: 'ReturnLOGOUT' in username)\n")
        username = display.styled_input(prompt= "username")
        if(username == "ReturnLOGOUT"):
            return None
        if auth.check_username(username):
            print("Username already taken! Try a different username!")
            input("Press Enter to Try again!")
            continue
        else:
            password = display.styled_input(prompt= "password")
            result = auth.register(username = username, password = password)
            return result

# -> login_ask(Decision: Guest) /Does its authentication using auth/
# Function Code Status: Complete Till Now
def guest():
    
    """
        This does nothing but returns the label as Guest for now
    """

    display.loading_animation(message= "Please wait!... Logging in as a Guest...", duration= 2)
    return "GUEST"




# ___________MENU SCREENS__________________________

# login_ask()-> main() /handsover the username and user type/ # -> menu(user) -> Download_Menu(user) {Download screens}
#                                                                             -> Bucket_menu() {Bucketlist screens}
#                                                                             -> History menu() {History Screens}
#                                                                             -> Settings_menu() {Settings screens}
# Function Code Status: Complete Till Now!
def menu(user):

    """
        This takes decision and send user data either logged menu or guest menu 
        and shows main menu differently for guest and logged_user.
        Tried to make the after codes of menu screens in soft coded as much as possible
    """
    
    if user[1] == "Logged User":
        options = {
            '1': ('DOWNLOAD MENU', download_menu),
            '2': ('BUCKET LIST', bucket_menu),
            '3': ('HISTORY', history_menu),
            '4': ('SETTINGS', settings_menu),
            '0': ('LOGOUT', None)
        }
        title = f"Hello! Welcome, {user[0]}\n* MAIN MENU {'='*15}"
    elif user[1] == "Guest User":
        options = {
            '1': ('DOWNLOAD MENU', download_menu),
            '0': ('LOGOUT', None)
        }
        title = f"Hello! Welcome, {user[0]}\n* GUEST MENU {'='*15}"
    else:
            # Fallback
            print("something went wrong!")
            input()

    while True:
        display.clear_screen()
        display.display_logo()
        
        
        # Build display dict (names only, no function references)
        # k for keys
        # v[0] for Display options
        display_options = {k: v[0] for k, v in options.items()}
        display.print_menu(title=title, options=display_options)
        if user[1] == "Guest User":
            print("Please login or register your account to use\nall the functionalities of the app!")

        choice = input("Enter your option:> ").strip()
        
        if choice not in options:
            print("Invalid option, try again")
            input()
            continue
            
        func = options[choice][1]
        if func is None:
            return  # logout
        func(user)  # call the function 



# __________DOWNLOAD SCREENS________________


# menu(user) -> download_menu(user) /takes different decisions/ -> /Guest and User have different menus/ -> /executes according to user input/
# Function Code Status: Complete Till Now
def download_menu(user):

    """
        This fn. do DIFFERENTIATE users according to their types.
        Guest users will have the minimalist options.
        User will have all the options, dynamically for presets in the menu
        User will choose from the menu.
    """


    # Base options available to everyone including guest
    options = {
        '1': ('QUICK DOWNLOAD - Built-in Presets', quick_download_ui.quick_download),
        '2': ('CUSTOM DOWNLOAD - Configure manually', custom_download_ui.custom_download),
        '0': ('BACK', None)
    }
    options2 = {
        '3' : ('CREATE PRESET - Save your config', create_presets),
        '4' : ('DELETE PRESET - Delete unnessecary configs', delete_presets)
        # '5' : ('RENAME PRESET - Rename your configs', rename_presets), # TODO: Will be built later
        # '6' : ('EDIT PRESET - Edit your configs', edit_presets), # TODO: Will be built later
    }

    # Logged users get profile options added dynamically
    if user[1] == "Logged User":
        options = options | options2
        # Runs a loop, calls load presets inside it and stores it in a separate dict. and ships it to the functions who need them like create, rename, delete
    while True:
        display.clear_screen()
        display.display_logo()

        title = "* DOWNLOADER"+"="*15

        # Build display dict (names only, no function references)
        # k for keys
        # v[0] for Display options
        display_options = {k: v[0] for k, v in options.items()}
        display.print_menu(title=title, options=display_options)

        choice = input("Enter your option:> ").strip()
        
        if choice not in options:
            print("Invalid option, try again")
            input()
            continue

        func = options[choice][1]
        if func is None:
            return  # logout
        func(user)  # call the function 



def create_presets(user):
    input("Hi this is create presets page")
    # call format string before saving
    #TODO: When creating a profile, block names that match built-in keys — add a check later.
    ...

def delete_presets(user):
    input("Hi this is delete presets page")
    ...
    
def rename_presets(user):
    input("Hi this is rename presets page")
    ...

def edit_presets(user):
    input("Hi this is edit presets page")
    # thinking to create a common editor for database called by every editing tasks
    ...



# __________BUCKETLIST SCREENS________________
def bucket_menu(user):
    ...



# __________HISTORY SCREENS___________________
def history_menu(user):
    ...


# __________SETTINGS SCREENS__________________
def settings_menu(user):
    ...


# if __name__ == "__main__":
#     ...