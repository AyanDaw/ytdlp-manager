RESOLUTION_TO_HEIGHT = {
    'audio only': None,
    '144p':  144,
    '240p':  240,
    '360p':  360,
    '480p':  480,
    '720p':  720,
    '1080p': 1080,
    '1440p': 1440,
    '2160p': 2160,
    '4320p': 4320
}

CODEC_TO_YTDLP = {
    'H.264':         'avc1',
    'H.265':         'hev1',
    'AV1':           'av01',
    'VP9':           'vp9',
    'No preference': None
}

# Data Simplifying tool functions

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
    else:
        return f"~ {bytes} Bytes"