import re

def modify_m3u8_playlist(m3u8_content):
    # Define your regex and manipulation logic for low quality here
    modified_playlist = re.sub(r'(.*360.*\n)|(.*Italian.*\n)', '', m3u8_content)
    # Add more manipulations as needed
    return modified_playlist

