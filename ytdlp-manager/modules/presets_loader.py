from modules import downloader
import database

# Tool function — not a page
# Called by: quick_download(user), custom_download(user), any download screen
# Returns: merged dict of built-in presets + user saved profiles
# Guest users only get built-in presets (get_profiles returns empty dict for guest)
def presets_loader(user) -> dict:

    """
        Combines built-in presets from downloader.py with user's saved profiles
        from the database into a single unified dict.
        Both built-ins and user profiles share the same dict structure:
        { 'name': ..., 'format': ..., 'merge_format': ... }
        so downstream code handles both identically.
        Built-ins always appear first, user profiles appended after.
    """

    default_presets = downloader.BUILTIN_PRESETS
    user_profiles = database.get_profiles(user[0])
    profiles = default_presets | user_profiles
    return profiles