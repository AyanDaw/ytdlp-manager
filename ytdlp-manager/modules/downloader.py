import yt_dlp
import display

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
    
if __name__ == "__main__":
    formats = get_formats(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    data = parse_formats(formats=formats)
    display.display_formats_table(formats=data)
    


# if user = "GUEST" skip all data based works like profiles
# For only youtube video and watchlist is available not for other platforms