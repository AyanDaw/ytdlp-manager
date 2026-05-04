from pathlib import Path
from modules import ensure_directory
import database


FILE_DIR = Path(__file__).parent # ytdlp-manager/modules
BASE_DIR = FILE_DIR.parent # ytdlp-manager

# Tool function — not a page
# Called by: quick_download(user), custom_download(user), any download screen
# Returns: validated download path string
# Priority: user input → user saved setting → system default
def get_download_path(user):
    """
        Determines where to save the downloaded file.
        Fallback chain (highest to lowest priority):
            1. Path entered by user right now
            2. User's saved default path from settings (database)
            3. System default: project/Downloads/username/
        Guest users skip input and go straight to system default.
        Creates the system default directory if it doesn't exist yet.
        Validates user-entered paths before accepting them.
    """
    
    DEF_DOWN_DIR = BASE_DIR / 'Downloads' / user[0] # Default download directory
    def_down_dir = str(DEF_DOWN_DIR) # Default download directory in str type
    DEF_DOWN_DIR.mkdir(parents=True, exist_ok=True)
    if user[1] == "Guest User":
        return def_down_dir  # program default

    print("\n(●'◡'●) NOTE: To ADD a Default-Path please visit to the Settings Page !!")
    print(f"\n(If the 'Default-Path' is not set then the Downloaded Items will be saved in System's Default-Path,\nWhich is: {def_down_dir})")
    print("\nType 'BACK' to Go Back...")
    while True:        
        print("\nO(∩_∩)O Press \'ENTER\' to Leave the Download-Path as Default as it is set in your settings")
        download_path = (input("Enter your Download-Path:> ")).strip()
        if download_path == 'BACK':
            return 'BACK'
        if download_path != "":
            try:
                ensure_directory.ensure_directory(download_path)
                return download_path
            except (PermissionError, ValueError, OSError) as e:
                print(f"Invalid path: {e}")
                input("Try again!")
                continue
        download_path = database.get_settings_data(username= user[0], key= 'download_folder')
        if download_path is not None:
            print(f"Using User default: {download_path}")
            input("Press Enter to continue...")
            return download_path
        else:
            print(f"Using system default: {def_down_dir}")
            input("Press Enter to continue...")
            return def_down_dir