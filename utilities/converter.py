def seconds_minutes(seconds):
    hours = int(seconds // 3600)  # 1 hour = 3600 seconds
    minutes = int((seconds % 3600) // 60)  # Remaining minutes
    seconds = int(seconds % 60)  # Remaining seconds
    if hours > 0:
        return f"{hours}:{minutes:02}m:{seconds:02}s"  # Ensures two-digit format for minutes and seconds
    else:
        return f"{minutes}m:{seconds:02}s"  # Exclude hours if it's 0