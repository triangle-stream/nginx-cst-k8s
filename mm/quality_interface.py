# quality_interface.py

def apply_quality_rules(m3u8_content, quality):
    # Import the specific quality module based on the quality level
    if quality == 'low':
        from low_quality import modify_m3u8_playlist
    elif quality == 'high':
        from high_quality import modify_m3u8_playlist
    else:
        # Handle unsupported quality levels
        return m3u8_content

    # Call the appropriate quality modification function
    return modify_m3u8_playlist(m3u8_content)

