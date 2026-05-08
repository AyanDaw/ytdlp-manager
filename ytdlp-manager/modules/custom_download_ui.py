from modules import display, fetcherNparser, downloader, get_download_path, file_opener
import sys
# from modules import file_opener TODO


# -> download_menu(Decision: Custom Download) -> custom_download(user)
# -> fetches formats -> user picks stream type -> picks FORMAT_IDs
# -> builds temp profile -> downloads
# Function Code Status: Complete Till Now
# TODO: Add BACK support to get_download_path()
# TODO: Ask for change URL in second stage (v1)
def custom_download(user):
    
    """
        Handles fully manual download configuration.
        Stage 1 (URL loop): Fetches available streams for the given URL.
            Loops until valid URL provided or user types BACK.
        Stage 2 (Selection loop): User picks stream type and FORMAT_IDs.
            Loops back to stream type selection on BACK or None return.
            Does NOT re-fetch formats — reuses Stage 1 data.
        Builds a temporary profile dict (not saved to database).
        Asks for fallback preference and merge format before downloading.
        Guest users supported — no profile saving involved.
    """

    while True:
        display.clear_screen()
        display.display_logo()

        title = "* CUSTOM DOWNLOAD"+"="*15
        display.print_menu(title=title, options=None)
        print("NOTE: 1 DOWNLOAD AT A TIME.\n\n(For multiple downloads try other download methods in Download page)\n")
        print("Enter 'BACK' at any Input-Section to return to the Download page!")
        url = input("Enter your media url:> ").strip()
        if url.upper() == 'BACK':
            return
        formats = fetcherNparser.get_formats(url=url)
        if formats is None:
            # print("Failed to fetch formats. Check your URL and connection.")
            input("Press Enter to try again...")
            continue
        cleaned_formats = fetcherNparser.parse_formats(formats=formats)
        break


    while True:
        display.clear_screen()
        display.display_logo()

        title = "* CUSTOM DOWNLOAD"+"="*15
        display.print_menu(title=title, options=None)        
        print(
"""
What are you downloading?

    1. Video + Audio (separate streams)
    2. Combined stream (video with audio already)
    3. Audio only
"""
            )
        
        while True:
            choice = input("Enter Your Choice:> ")
            if choice.upper() == "BACK":
                return
            
            if choice not in ("1", "2", "3"):
                print("Invalid option, try again")
                input()
                continue
            else:
                break
        if choice == "1":
            download_string = separate_downloader_str(formats=cleaned_formats)
        elif choice == "2":
            download_string = combined_downloader_str(formats=cleaned_formats)
        elif choice == "3":
            download_string = audio_only_downloader_str(formats=cleaned_formats)

        if download_string is None:
            continue  # back to "what are you downloading?" screen

        fallback_ask = input("Want a Fall Back if something Stream related Goes Wrong?? [Y/n]:>")
        if fallback_ask.upper() == 'BACK':
            return
        if fallback_ask.strip().lower() in ('y', 'yes', ''):
            download_string += "/best"
        # Build temp profile dict
        print("Select merge format:")
        print("1. mp4 (recommended)") # TODO: As for upto ver1, until multi stream feature is added.
        print("2. mkv")
        print("3. webm")
        merge_choice = input("Enter choice (or press Enter for mp4):> ").strip()
        merge_map = {'1': 'mp4', '2': 'mkv', '3': 'webm'}
        merge_format = merge_map.get(merge_choice, 'mp4')

        temp_profile = {
            'name': 'Custom',
            'format': download_string,
            'merge_format': merge_format
        }

        download_path = get_download_path.get_download_path(user)
        
        if download_path == 'BACK':
            return
        
        result = downloader.download(url=url, profile=temp_profile, download_folder=download_path)
        print(result[1])  # show "Download successful" or error message
        if result[0]:
            response = file_opener.open_file(result[2])
            if not response:
                print("\nSorry unable to open the file/folder (┬┬﹏┬┬)")
            else:
                exit_ok = input("Want to exit the App? [Y/n]:> ")
                if exit_ok.strip().lower() in ('y', 'yes', ''):
                    display.clear_screen()
                    display.display_logo()
                    display.loading_animation(message= "Exiting...", duration= 1)
                    print("\nHave a good day!... :)")
                    sys.exit()
            
        input("Press Enter to continue...")
        break  # exit the while loop after successful download
    display.loading_animation(message="Returning to Download Menu...", duration=0.5)
    return


# -> custom_download() -> separate_downloader_str(formats)
# -> filters video and audio streams separately
# -> collects FORMAT_IDs from user -> returns yt-dlp format string
# Function Code Status: Complete (Multi-audio support planned for v1.0)
# This is a Page part not a standalone Page.
def separate_downloader_str(formats: list) -> str:

    """
        Filters the cleaned format list into separate video-only and audio-only streams.
        Displays each table separately for user to pick FORMAT_IDs from.
        User picks a video stream ID (required) and an audio stream ID (optional).
        Returns a yt-dlp compatible format string:
            - With audio: 'video_id+audio_id'
            - Without audio: 'video_id'
        Note: Combined streams (having both vcodec and acodec) are excluded here.
        Note: Multi-audio stream support is planned for v1.0
    """

    video_formats = []
    audio_formats = []
    for id in formats:
        if id['VCODEC'] != 'none' and id['ACODEC'] == 'none':
            video_formats.append(id) 
        if id['VCODEC'] == 'none' and id['ACODEC'] != 'none':
            audio_formats.append(id)
        if (id['VCODEC'] == 'none' and id['ACODEC'] == 'none') or (id['VCODEC'] != 'none' and id['ACODEC'] != 'none'):
            continue

    # show the formats with ids
    # videos
    if not video_formats:
        print("Sorry There's no Video Only Streams... :( ")
        return None
    
    print("\nChoose a FORMAT_ID of a Video Stream from below table:\n")
    display.display_formats_table(formats=video_formats)
    while True:
        video_part_id = input("Enter Your Choice (Leave empty to choose the best):>")
        if video_part_id.upper() == 'BACK':
            return None  # caller handles None as "user went back"
        
        valid_ids = [f['FORMAT_ID'] for f in video_formats]

        if video_part_id == "":
            video_part_id = "bestvideo"
            break

        elif video_part_id not in valid_ids:
            print("There's no such FORMAT_ID there! Try Again Please!")
            input("Press 'Enter' to input Format_ID Again!")
            continue
        else:
            sure_ok = input(f"Are you sure you want to Download the FORMAT_ID '{video_part_id}'? [Y/n]:")
            if sure_ok.upper() == 'BACK':
                return None  # caller handles None as "user went back"
            if sure_ok.strip().lower() in ('y', 'yes', ''):
                break
            else:
                continue

    # audios
    if not audio_formats:
        print("Sorry There's no Audio Only Streams... :( ")
        return None
    
    print("\nNow choose a FORMAT_ID of a Audio Stream from below table:\n")
    display.display_formats_table(formats=audio_formats)
    while True:
        audio_part_id = input("Enter Your Choice (Leave empty to choose the best, Type 'NONE' for no audio):>")
        if audio_part_id.upper() == 'BACK':
            return None  # caller handles None as "user went back"
        if audio_part_id.upper() == 'NONE':
            audio_part_id = None
        valid_ids = [f['FORMAT_ID'] for f in audio_formats]

        if audio_part_id == "":
            audio_part_id = "bestaudio"
            break
        elif audio_part_id not in valid_ids:
            print("There's no such FORMAT_ID there! Try Again Please!")
            input("Press 'Enter' to input Format_ID Again:> ")
            continue
        else:
            sure_ok = input(f"Are you sure you want to Download the FORMAT_ID '{audio_part_id}'? [Y/n]:")
            if sure_ok.upper() == 'BACK':
                return None  # caller handles None as "user went back"
            if sure_ok.strip().lower() in ('y', 'yes', ''):
                break
            else:
                continue

    format_string = video_part_id
    if audio_part_id == None:
        return format_string
    else:
        return format_string + f"+{audio_part_id}"


# -> custom_download() -> combined_downloader_str(formats)
# -> filters combined streams (having both video and audio)
# -> collects FORMAT_ID from user -> returns yt-dlp format string
# Function Code Status: Complete (Single result auto-select planned for v1.0)
def combined_downloader_str(formats: list) -> str:

    """
        Filters the cleaned format list for combined streams only —
        streams that already contain both video and audio.
        Displays the filtered table for user to pick a FORMAT_ID from.
        Returns the FORMAT_ID string directly — no merging needed.
        Returns None if:
            - No combined streams available
            - User typed BACK at any input point
        Note: Auto-select when only one stream available planned for v1.0
    """

    combined_formats = []

    for id in formats:
        if id['VCODEC'] != 'none' and id['ACODEC'] != 'none':
            combined_formats.append(id) 
        else:
            continue
    
    # Not found case
    if not combined_formats:
        print("Sorry There's no Combined Streams... :( ")
        input("Press 'Enter' to check other options")
        return None
    
    # Found only one case
    # elif
    # Not wanting to make now, Leaving it for TODO:.

    # Found Case
    else:
        # show the formats with ids
        # Combined
        print("\nChoose a FORMAT_ID of a Stream from below table:\n")
        display.display_formats_table(formats=combined_formats)

        while True:
            combined_id = input("Enter Your Choice:>")
            if combined_id.upper() == 'BACK':
                return None  # caller handles None as "user went back"
            valid_ids = [f['FORMAT_ID'] for f in combined_formats]
            if combined_id == "":
                combined_id = 'best'
                break

            elif combined_id not in valid_ids:
                print("There's no such FORMAT_ID there! Try Again Please!")
                input("Press 'Enter' to input Format_ID Again:> ")
                continue
            else:
                sure_ok = input(f"Are you sure you want to Download the FORMAT_ID '{combined_id}'? [Y/n]:")
                if sure_ok.upper() == 'BACK':
                    return None  # caller handles None as "user went back"
                if sure_ok.strip().lower() in ('y', 'yes', ''):
                    break
                else:
                    continue

    format_string = combined_id
    return format_string


# -> custom_download() -> audio_only_downloader_str(formats)
# -> filters audio-only streams (no video codec)
# -> collects FORMAT_ID from user -> returns yt-dlp format string
# Function Code Status: Complete (Single result auto-select planned for v1.0)
def audio_only_downloader_str(formats: list) -> str:

    """
        Filters the cleaned format list for audio-only streams —
        streams that have no video codec but have an audio codec.
        Displays the filtered table for user to pick a FORMAT_ID from.
        Returns the FORMAT_ID string directly.
        Returns None if:
            - No audio-only streams available
            - User typed BACK at any input point
        Note: Auto-select when only one stream available planned for v1.0
    """

    audio_only_formats = []

    for id in formats:
        if id['VCODEC'] == 'none' and id['ACODEC'] != 'none':
            audio_only_formats.append(id) 
        else:
            continue
    
    # Not found case
    if not audio_only_formats:
        print("Sorry There's no Audio Only Streams... :( ")
        input("Press 'Enter' to check other options")
        return None
    
    # Found only one case
    # elif
    # Not wanting to make now, Leaving it for TODO:.

    # Found Case
    else:
        # show the formats with ids
        # Combined
        print("\nChoose a FORMAT_ID of a Stream from below table:\n")
        display.display_formats_table(formats=audio_only_formats)

        while True:
            audio_only_id = input("Enter Your Choice:>")
            if audio_only_id.upper() == 'BACK':
                return None  # caller handles None as "user went back"
            valid_ids = [f['FORMAT_ID'] for f in audio_only_formats]
            if audio_only_id == "":
                audio_only_id = "bestaudio"
                break

            elif audio_only_id not in valid_ids:
                print("There's no such FORMAT_ID there! Try Again Please!")
                input("Press 'Enter' to input Format_ID Again:> ")
                continue
            else:
                sure_ok = input(f"Are you sure you want to Download the FORMAT_ID '{audio_only_id}'? [Y/n]:")
                if sure_ok.upper() == 'BACK':
                    return None  # caller handles None as "user went back"
                if sure_ok.strip().lower() in ('y', 'yes', ''):
                    break
                else:
                    continue

    format_string = audio_only_id
    return format_string