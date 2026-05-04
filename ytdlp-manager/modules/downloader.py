import yt_dlp
import os
import time

from modules import display, build_format_string
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DOWNLOAD_DIR = BASE_DIR /'Downloads'

COOKIE_DIR = BASE_DIR / 'Cookies' # TODO Later we will make it divided by user, dynamic path got by another place

BUILTIN_PRESETS = {
    'best': {
        'name': 'Best Quality',
        'format': 'bestvideo+bestaudio/best',
        'merge_format': 'mp4'
    },
    'audio': {
        'name': 'Audio Only',
        'format': 'bestaudio/best',
        'merge_format': 'mp3'
    },
    'lightweight': {
        'name': 'Lightweight (720p)',
        'format': 'bestvideo[height<=720]+bestaudio/best',
        'merge_format': 'mp4'
    }
}

last_update = 0

"""
    What download_status is
        
        download_status is the dictionary yt-dlp automatically passes to your hook function every time download
        progress updates. You don't create it — yt-dlp creates it and sends it to your function.
        It looks something like this during download:

        {
            'status': 'downloading',
            '_percent_str': ' 45.3%',
            '_speed_str': '1.23MiB/s',
            '_eta_str': '00:12',
            'filename': 'video.mp4'
        }

        And when finished:

        {
            'status': 'finished',
            'filename': 'video.mp4'
        }
"""

# downloading functions
def download(url, profile, download_folder):
    cookie_path = Path(COOKIE_DIR) / 'cookies.txt'
    # TODO make cookie file inputable and conditional
    ydl_opts = {
    'format': profile['format'],
    'merge_output_format': profile.get('merge_format', 'mp4'),
    'outtmpl': str(Path(download_folder) / "%(title)s.%(ext)s"),
    'quiet': True,
    'no_warnings': False,
    'noprogress' : True,
    'progress_hooks': [progress_hook]
    }

    if cookie_path.exists():
        ydl_opts['cookiefile'] = str(cookie_path)

    print(f"Downloading to: {download_folder}")
    

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url= url, download= False)
            filename_full = ydl.prepare_filename(info)
            print(f"\n[DOWNLAODING...]: '{filename_full}'")

            # replace download() with process_info() but thats need restructuring.
            ydl.process_info(info) 
        #TODO: Return download folder when its multiple videos
        return (True, "Download successful", filename_full)
    except yt_dlp.utils.DownloadError as e:
        return (False, f"Download failed: {e}", None)


def progress_hook(download_status):

    global last_update
    filename_full = os.path.basename(download_status.get('filename', "FileName"))
    
    def truncate(string: str, max_length: int) -> str:
        if len(string) <= max_length:
            return string
        return string[:max_length - 3] + "..."
    

    def progress_barNpercentage(downloaded_size: float, total_size: float, width: int) -> str:
        portion = downloaded_size/total_size
        filled = int(width * portion)
        percentage_float = (downloaded_size/total_size) * 100
        not_filled = width - filled
        bar = "#" * filled + "-" * not_filled
        return f":> [{bar}] {percentage_float:.2f}%"
        # [#########---------------------]


    def seconds_to_hms_str(seconds: int | float) -> str:
        seconds = int(seconds or 0)

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        elif (h == 0) and (m > 0):
            return f"{m:02d}:{s:02d}"
        else:
            return f"{s:02d} secs"


    """
status: the downloading status
info_dict:
filename: the name of the file is available
tmpfilename: the temporary file name
downloaded_bytes: Bytes on disk
total_bytes: Total size of files
total_bytes_estimate: Total estimated size 
elapsed: The number of seconds since download started.
eta: The estimated time in seconds, None if unknown
speed: The download speed in bytes/second, None if unknown
fragment_index: The counter of the currently downloaded video fragment.
fragment_count: The number of fragments (= individual files that will be merged)
noprogress: Do not print the progress bar
    """
    
    
    if download_status['status'] == 'downloading':

        now = time.time()
        if now - last_update < 0.1:  # update every 100ms max
            return
        last_update = now

        # filename = truncate(filename_full, 25)
        downloaded_bytes = (download_status.get('downloaded_bytes', 0))/(1024*1024)
        total_bytes = (download_status.get('total_bytes') or 0)/(1024*1024)
        elapsed = download_status.get('elapsed') or 0
        elapsed_str = seconds_to_hms_str(seconds= elapsed)
        eta = download_status.get('eta') or 0
        eta_str = seconds_to_hms_str(seconds= eta)
        speed = (download_status.get('speed') or 0)/(1024*1024) # in MB
        speed_str = f"{speed:.2f} MB/s"
        progress_bar_percentage = progress_barNpercentage(downloaded_size= downloaded_bytes, total_size= total_bytes, width= 30)

        
        # TODO: Make conditional MB, GB etc.
        print(f"\r{progress_bar_percentage} | {downloaded_bytes:.2f}/{total_bytes:.2f} MB | Elapsed: {elapsed_str} | ETA: {eta_str} | ↓: {speed_str}", " "*20, end= " ", flush= True)
        
    elif download_status['status'] == 'finished':
        print("\nProcessing...", " "*20)  # more accurate — merging happens after
        # TODO: later we will send all these values to ui to print using display module
        # For now we are printing here
    
    elif download_status['status'] == 'error':
        print(f"\nError during download")


if __name__ == "__main__":
    # url="https://www.youtube.com/watch?v=CNDBIFpOCVI" # Rick-Roll Video's link
    # formats = get_formats(url=url)
    # data = parse_formats(formats=formats)
    # display.display_formats_table(formats=data)
    # format_id = input("Enter id: ").strip()
    # download_folder = str(DOWNLOAD_DIR)
    # download(url=url, profile= BUILTIN_PRESETS['best'], download_folder=download_folder)
    # print(build_format_string("1080p", "H.264", True, True))
    # print(build_format_string('audio only', None, True, True))
    # print(build_format_string('720p', 'No preference', True, False))
    print(build_format_string.build_format_string('1080p', 'AV1', False, True))
    # print(build_format_string('2160p', 'VP9', True, True))


# TODO: if user = "GUEST" skip all data based works like profiles
# TODO: For only youtube video and watchlist is available not for other platforms.