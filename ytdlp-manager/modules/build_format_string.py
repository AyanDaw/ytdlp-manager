from modules import converter


# STATUS = Building complete for now
def build_format_string(video_res: str, codec: str, audio_ok: bool, fallback_ok: bool) -> str:
    # This Function is made for coversion that converts human readable info ytdlp suitable format.
    # Handling audio only
    if video_res == 'audio only':
        if fallback_ok:
            return "bestaudio/best"
        return'bestaudio'
    # get height
    height = converter.RESOLUTION_TO_HEIGHT.get(video_res)
    if height is None:
        format_string = 'bestvideo+bestaudio' # Its Safer than sorry
    
    # get codec
    codec_code = converter.CODEC_TO_YTDLP.get(codec)
    if codec_code is None:
        video_part = f'bestvideo[height<={height}]'
    else:
        video_part = f'bestvideo[height<={height}][vcodec^={codec_code}]'

    # audio contion
    if audio_ok:
        format_string = f'{video_part}+bestaudio'
    else:
        format_string = video_part

    # add fallback if allowed
    if fallback_ok:
        format_string = f"{format_string}/best"

    return format_string