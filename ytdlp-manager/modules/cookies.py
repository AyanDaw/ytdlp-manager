import sys
import file_opener
import ensure_directory
# from modules import ensure_directory
# from modules import file_opener
from pathlib import Path
# from colorama import Fore, Back, Style . Dont know how to use T-T


BASE_DIR = Path(__file__).resolve().parent.parent
COOKIE_DIR = BASE_DIR / "Cookies"

def create_cookie(username: str, cookiepath: Path, platform: str) -> bool:

    """
    creates cookie file in app directory.
    reads the provided file.
    If every thing is ok, then creates the file.
    NOTE:
    The path should be already sanitized from caller
    ask_cookie_path() sanitizes and provides the cookie_path got from user
    """

    USER_COOKIE_DIR = COOKIE_DIR / username
    platform = platform.strip().lower().replace(" ", "")

    cookie_content = ""
    try:
        # Tries to read the file
        with open(cookiepath, "r") as cookie_r:
            cookie_content = cookie_r.read()
    except OSError as e:
        print(e)
        input()
        return False

    if not cookie_content.startswith("# Netscape HTTP Cookie File"):
        print("[ERROR]:", "The given cookie file is in invalid format!") # TODO: here i want to use it with the error text only and safely just for this print, and the "error" word only
        input()
        return False
    
    cookie_file_name = f"{cookie_name(username=username, platform=platform, cookie_folder=USER_COOKIE_DIR)}.txt"
    cookie_file_path = USER_COOKIE_DIR / cookie_file_name

    try:
        USER_COOKIE_DIR.mkdir(parents=True, exist_ok=True)
        with open (cookie_file_path, "w", encoding="utf-8") as cookie_w:
            cookie_w.write(cookie_content)
            return True
    except OSError as e:
        print(e)
        input()
        return False

def cookie_name(username: str, platform: str, cookie_folder: Path) -> str:
    """
    Genarates cookie file name after checking if it is already occupied or not
    """

    USER_COOKIE_DIR = cookie_folder
    def is_cookie(filename: str) -> bool:
        "Checks name availibilty. If available then True, else if occupied then False"
        "Ignore the Max 3 File rule"

        cookie_file_path = USER_COOKIE_DIR / f"{filename}.txt"
        return not cookie_file_path.exists()
        # Checking if already a file is available with this name

    if not platform:
        filename = f"{username}"
    else:
        filename = f"{username}-{platform}"

    base_filename = filename  # save original before loop
    count = 1
    while True:
        if is_cookie(filename=filename):
            break
        filename = f"{base_filename}_({count})"
        count += 1

    return filename

def ask_cookie_path():
    "A ui-cookie function"
    # TODO: move this fnction to ui.cookie or cookie_ui.py
    "get_cookie_path is now ask_cookie_path"
    "asks user for file path, strips quotes, BACK support"

def ensure_cookie():
    "checks existence, returns path or None"
    
def cookie_guide():
    "shows export guide, user picks browser"

def delete_cookie(user):
    "shows list, user picks, confirms, deletes"

def list_cookies(user):
    "returns all cookie files for that user"

def cookie_menu(user):
    "The page, dispatch table"
    "This function should be handled by ui.cookie_menu() or cookie_ui.py"

if __name__ == "__main__":
        
    # TEST: 1
        while True:
            cookie_path = input("Enter path:> ").strip().strip('"').strip("'")
            if cookie_path == 'BACK':
                sys.exit()
                # return None in actual ui
            cookie_Path = Path(cookie_path)
            platform = input("Enter Platform:> ")
            if platform == 'BACK':
                sys.exit()
                # return None actual ui
            if create_cookie(username="Test-User", cookiepath=cookie_Path, platform=platform):
                print("cookie succesfully created")
                break
            else:
                print("cookie is not succesfully created")
                input()

    # TEST #:
        #
    # TODO: For now as support only youtube till now
    # TODO: It will be handled by ui.cookie_menu() or cookie_ui.py