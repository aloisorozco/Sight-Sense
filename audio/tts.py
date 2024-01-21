import os
import torch
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import time
import pyaudio
import wave
from . import spatial

CACHE_DIR = os.path.join(os.getcwd(), "cache")
AUDIO_CHUNK_SIZE = 1024

# ----- MODULE SETUP ------

if not os.path.isdir(CACHE_DIR):
    os.mkdir(CACHE_DIR)

# --- MODULE SETUP END ----

class tts_config:
    def __init__(self):
        self.speaker_embedding = None
        self.synthesiser = None


def create_config():
    synthesiser = load_model()
    speaker_embedding = load_speaker()

    config = tts_config()
    config.speaker_embedding = speaker_embedding
    config.synthesiser = synthesiser

    return config


def load_model():
    model = pipeline("text-to-speech", "microsoft/speecht5_tts")
    return model


def load_speaker():
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
    return speaker_embedding


def speak(text, model, speaker_embedding):
    # measure time consumption
    start = time.time()

    # synthesise speech with the speaker's embedding
    speech = model(text, forward_params={"speaker_embeddings": speaker_embedding})

    end = time.time()
    print("Keyword " + text + ", was read in " + str(end - start) + "s.")
        
    return speech


def play_audio_once(audio_path):
    f = wave.open(audio_path, "rb")  

    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(AUDIO_CHUNK_SIZE)  
    
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(AUDIO_CHUNK_SIZE)  
    
    #stop stream  
    stream.stop_stream()  
    stream.close()  
    
    #close PyAudio  
    p.terminate() 


def try_generate(keyword, config):
    keyword_file_path = os.path.join(CACHE_DIR, str.lower(keyword) + ".wav")

    # checks if the file corresponding to the keyword exists, to avoid regenerating it
    if not os.path.isfile(keyword_file_path):
        print("Generating file for keyword " + keyword + "...")
        speech = speak(keyword, config.synthesiser, config.speaker_embedding)
        
        sf.write(keyword_file_path, speech["audio"], samplerate=speech["sampling_rate"])

    return keyword_file_path


def generate_and_play(keyword, config):
    path = try_generate(keyword, config)

    # plays the file corresponding to the keyword
    print("Playing file for keyword " + keyword + "...")
    play_audio_once(path)


def generate_and_play_spatial(keyword, config, x, y, spatial_config):
    path = try_generate(keyword, config)

    # plays the file corresponding to the keyword
    print("Playing spatial file for keyword " + keyword + "...")
    
    panned_audio_path = spatial.generate_spatial_audio(path, x, y, spatial_config)
    play_audio_once(panned_audio_path)

    # we remove the panned audio file after playing it, because it's coordinate specific
    os.remove(panned_audio_path)
    

def test():
    tts_config = create_config()

    keywords = ["Human", "Door", "Dog", "Bike", "Construction", "Car", "Cat", "Traintracks", "Puddle", "Fire"]
    
    for keyword in keywords:
        time.sleep(0.5)
        generate_and_play(keyword, tts_config)

def test_spatial():
    MAX_X = 1000
    MAX_VOLUME_PARANTHESES_MAYBE_Z_PARANTHESES = 1000

    tts_config = create_config()
    spatial_config = spatial.create_spatial_config(MAX_X, MAX_VOLUME_PARANTHESES_MAYBE_Z_PARANTHESES)

    keywords = ["Human", "Door", "Dog", "Bike", "Construction", "Car", "Cat", "Traintracks", "Puddle", "Fire"]
    
    i = 0
    for keyword in keywords:
        time.sleep(0.5)
        
        generate_and_play_spatial(keyword, tts_config, MAX_X / len(keywords) * i, MAX_VOLUME_PARANTHESES_MAYBE_Z_PARANTHESES, spatial_config)
        
        i += 1