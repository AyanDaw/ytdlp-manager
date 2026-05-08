from pathlib import Path
from modules import converter
import yt_dlp



BASE_DIR = Path(__file__).resolve().parent.parent

COOKIE_DIR = BASE_DIR / 'Cookies' # TODO Later we will make it divided by user, dynamic path got by another place

# Real functions
def get_formats(url: str) -> list:

    try:
        opts = {
            'quiet': True,
            'remote_components': {'ejs:github'}
        }
        if COOKIE_DIR.exists():
            cookie_file = COOKIE_DIR / 'cookies.txt'
            if cookie_file.exists():
                opts['cookiefile'] = str(cookie_file)
        # TODO make it conditional
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info.get('_type') == 'playlist':
                print("Playlist URLs are not supported in Custom Download. Please enter a single video URL.")
                return None
            return info.get('formats', [])
    except yt_dlp.utils.DownloadError as e:
        error_str = str(e).lower()
        if "sign in" in error_str or "age" in error_str:
            print("This video requires login or age verification.")
        elif "not available" in error_str:
            print("This video is unavailable — may be region-locked or Kids content.")
        else:
            print(f"Could not fetch formats: {e}")
        return None
    
def parse_formats(formats: list) -> list:
    cleaned_formats= []
    for f in formats:
        if f.get('ext') == 'mhtml':
            continue
        cleaned_formats.append({
            'FORMAT_ID': f.get('format_id'),
            'EXT':       f.get('ext'),
            'RESOLUTION': converter.simplify_resolution(f.get('resolution')),
            'ACODEC':    converter.simplify_codec(f.get('acodec')),
            'VCODEC':    converter.simplify_codec(f.get('vcodec')),
            'FILESIZE':  converter.format_filesize(f.get('filesize'))
        })

    return cleaned_formats