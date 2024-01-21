from pydub import AudioSegment

class spatial_config:
    def __init__(self):
        self.max_x = None
        self.max_y = None

def create_spatial_config(max_x, max_volume_parantheses_maybe_z_parantheses):
    config = spatial_config()
    config.max_x = max_x
    config.max_volume_parantheses_maybe_z_parantheses = max_volume_parantheses_maybe_z_parantheses

    return config

def generate_spatial_audio(file_name, x, volume_parantheses_maybe_z_parantheses, config):
    # Load your audio file
    audio_file = AudioSegment.from_file(file_name, format="wav")

    # Calculate panning based on x coordinate
    pan = (x / config.max_x) * 2 - 1  # Map x coordinate to range -1 to 1
    print(pan)
    # Apply panning to audio
    panned_audio = audio_file.pan(pan)

    # Adjust volume based on y coordinate
    volume = int((volume_parantheses_maybe_z_parantheses / config.max_volume_parantheses_maybe_z_parantheses) * 100)  # Map y coordinate to range 0 to 100
    panned_audio = panned_audio - (100 - volume)

    # Export the processed audio file
    panned_audio_path = file_name[:-3] + "_panned.wav"
    panned_audio.export(panned_audio_path, format="wav")

    return panned_audio_path
