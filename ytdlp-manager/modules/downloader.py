import yt_dlp
import display
from pathlib import Path


DOWNLOAD_DIR = Path(__file__).parent.parent / 'Downloads'


# Data Simplifications
def simplify_resolution(resolution: str) -> str:
    match resolution:
        case "audio only":
            return "audio only"
        case "256x144":
            return "144P"
        case "426x240":
            return "240P"
        case "640x360":
            return "360P"
        case "854x480":
            return "480P (SD)"
        case "1280x720":
            return "720P (HD)"
        case "1920x1080":
            return "1080P (FHD)"
        case "2560x1440":
            return "1440P (QHD)"
        case "3840x2160":
            return "2160P (4K)"
        case "7680x4320":
            return "4320P (8K)"
        case _:
            return resolution  # show raw if unknown

def simplify_codec(codec: str) -> str:
    if codec is None or codec == 'none':
        return 'none'
    if 'avc' in codec:
        return 'H.264'
    if 'hev' in codec or 'hvc' in codec:
        return 'H.265'
    if 'av01' in codec:
        return 'AV1'
    if 'vp9' in codec:
        return 'VP9'
    if 'mp4a' in codec:
        return 'AAC'
    if 'opus' in codec:
        return 'Opus'
    return codec  # fallback: show raw if unknown

def format_filesize(bytes: int) -> str:
    if bytes == None:
        return "Unknown"
    elif bytes >= 1024**3:
        gb = bytes/(1024**3)
        return f"~ {gb:.2f} GB"
    elif bytes >= 1024**2:
        mb = bytes/(1024**2)
        return f"~ {mb:.2f} MB"
    elif bytes >= 1024:
        kb = bytes/1024
        return f"~ {kb:.2f} KB"



# Real functions
def get_formats(url: str):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('formats', [])
    except yt_dlp.utils.DownloadError as e:
        print(f"Failed to fetch formats: {e}")
        return None
        
def parse_formats(formats):
    cleaned_formats= []
    for f in formats:
        if f.get('ext') == 'mhtml':
            continue
        cleaned_formats.append({
            'FORMAT_ID': f.get('format_id'),
            'EXT':       f.get('ext'),
            'RESOLUTION': simplify_resolution(f.get('resolution')),
            'ACODEC':    simplify_codec(f.get('acodec')),
            'VCODEC':    simplify_codec(f.get('vcodec')),
            'FILESIZE':  format_filesize(f.get('filesize'))
        })

    return cleaned_formats


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

def download(url, format_id, download_folder):
    ydl_opts = {
    'format': format_id,
    # 'outtmpl': f'{download_folder}/video.%(ext)s',
    'outtmpl': str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
    'quiet': True,
    'noprogress' : True,
    'progress_hooks': [progress_hook]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return (True, "Download successful")
    except yt_dlp.utils.DownloadError as e:
        return (False, f"Download failed: {e}")

def progress_hook(download_status):
    if download_status['status'] == 'downloading':
        percentage_str = download_status.get('_percent_str', '?')
        # percentage_int = int(float(percentage_str.strip().replace('%', '')))
        # outof20 = 20*percentage_int
        speed = download_status.get('_speed_str', '?')
        eta = download_status.get('_eta_str', '?')
        filename = download_status.get('filename','video.mp4')
        # later we will send all these values to ui to print using display module
        # For now we are printing here
        print(f"{percentage_str} | {speed} | ETA: {eta}", " "*10, end= "\r")

    elif download_status['status'] == 'finished':
        print("Download complete!", " "*20)
    
if __name__ == "__main__":
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Rick-Roll Video's link
    formats = get_formats(url=url)
    data = parse_formats(formats=formats)
    display.display_formats_table(formats=data)
    format_id = input("Enter id: ").strip()
    download_folder = str(DOWNLOAD_DIR)
    download(url=url, format_id=format_id, download_folder=download_folder)


# if user = "GUEST" skip all data based works like profiles
# For only youtube video and watchlist is available not for other platforms