from pydub import AudioSegment
import os

class spatial_config:
    def __init__(self):
        self.max_x = None
        self.max_y = None

def create_spatial_config(max_x, max_y):
    config = spatial_config()
    config.max_x = max_x
    config.max_y = max_y

    return config

def generate_spatial_audio(file_name, x, y, config):
    # Load your audio file
    audio_file = AudioSegment.from_file(file_name, format="wav")

    # Calculate panning based on x coordinate
    pan = (x / config.max_x) * 2 - 1  # Map x coordinate to range -1 to 1
    print(pan)
    # Apply panning to audio
    panned_audio = audio_file.pan(pan)

    # Adjust volume based on y coordinate
    volume = int((y / config.max_y) * 100)  # Map y coordinate to range 0 to 100
    panned_audio = panned_audio - (100 - volume)

    # Remove the old file
    os.remove(file_name)

    # Export the processed audio file
    panned_audio.export(file_name, format="wav")