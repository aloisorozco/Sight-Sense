from pydub import AudioSegment
import pyaudio
import wave
import numpy as np
import os

def generate_spatial_audio(x, y, object_name):
    # Load your audio file
    audio_file = AudioSegment.from_file("audio.wav", format="wav")

    # Calculate panning based on x coordinate
    pan = (x / max_x) * 2 - 1  # Map x coordinate to range -1 to 1
    print(pan)
    # Apply panning to audio
    panned_audio = audio_file.pan(pan)

    # Adjust volume based on y coordinate
    volume = int((y / max_y) * 100)  # Map y coordinate to range 0 to 100
    panned_audio = panned_audio - (100 - volume)

    # Export the processed audio
    panned_audio.export(f"{object_name}_spatial_audio.wav", format="wav")

    return f"{object_name}_spatial_audio.wav"

def play_audio(file_path):
    # Set up audio playback
    p = pyaudio.PyAudio()
    chunk = 1024
    wf = wave.open(file_path, 'rb')
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Play audio
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

# Example usage
max_x = 1280  # Maximum x coordinate in your image
max_y = 1080  # Maximum y coordinate in your image

# Replace these values with the actual x, y coordinates and object name
x_coordinate = 800
y_coordinate = 1080
object_name = "example_object"

audio_file_path = generate_spatial_audio(x_coordinate, y_coordinate, object_name)
play_audio(audio_file_path)

os.remove("example_object_spatial_audio.wav")