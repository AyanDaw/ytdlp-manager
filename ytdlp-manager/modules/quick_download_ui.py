from modules import display, downloader
from modules import presets_loader, get_download_path, file_opener
import sys


# -> download_menu(Decision: Quick Download) -> quick_download(user)
# -> user picks preset -> downloader.download() -> returns result
# Function Code Status: Complete Till Now
def quick_download(user):

    """
        Shows combined preset menu (built-in presets + user saved profiles).
        User picks a preset, enters URL, chooses download path.
        Hands off to downloader.download() with the full profile dict.
        Does NOT ask format questions — preset handles all format decisions.
        Guest users see only built-in presets (no saved profiles).
        Logged users see built-ins + their saved profiles merged together.
    """

    options = presets_loader.presets_loader(user)
    
    display_options = {}
    key_map = {}  # maps display number to options key
    i = 1
    for key in options:
        display_options[str(i)] = options[key]['name']
        key_map[str(i)] = key  # store actual key
        i += 1
    display_options['0'] = 'Back'

    while True:
        display.clear_screen()
        display.display_logo()

        title = "* QUICK DOWNLOAD"+"="*15

        display.print_menu(title=title, options=display_options)
        print("\nType 'BACK' in any input to go BACK...")
        choice = input("Enter your option:> ").strip()
        
        if choice == 'BACK':
            return
        
        if choice not in display_options:
            print("Invalid option, try again")
            input()
            continue

        if choice == '0':
            return
        

        url = input("Enter url of the video/playlist : ")
        
        if url == 'BACK':
            return

        selected_key = key_map[choice]
        download_format = options[selected_key]
        # Nothing goes except a dict having format, mergeformat, name. the key doesnt got with it.

        download_path = get_download_path.get_download_path(user)

        if download_path == 'BACK':
            return
        
        print(f"Downloading to: {download_path}")
        result = downloader.download(url= url, profile= download_format, download_folder= download_path)

        print(result[1])
        if result[0]:
            response = file_opener.open_file(result[2])
            if not response:
                print("\nSorry unable to open the file/folder (┬┬﹏┬┬)")
            else:
                exit_ok = input("Want to exit the App? [Y/n]:> ")
                if exit_ok.strip().lower() in ('y', 'yes', ''):
                    sys.exit()
    
        input("Press Enter to continue...")
        return
        # now loop refreshes and returns to previous page