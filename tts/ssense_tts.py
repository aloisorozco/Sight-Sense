import os
import torch
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import time
import pyaudio
import wave

CACHE_DIR = os.path.join(os.getcwd(), "cache")
AUDIO_CHUNK_SIZE = 1024

if not os.path.isdir(CACHE_DIR):
    os.mkdir(CACHE_DIR)

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

def read_and_play(keyword, config):
    keyword_file_path = os.path.join(CACHE_DIR, str.lower(keyword) + ".wav")

    # checks if the file corresponding to the keyword exists, to avoid regenerating it
    if not os.path.isfile(keyword_file_path):
        print("Generating file for keyword " + keyword + "...")
        speech = speak(keyword, config.synthesiser, config.speaker_embedding)
        sf.write(keyword_file_path, speech["audio"], samplerate=speech["sampling_rate"])

    # plays the file corresponding to the keyword
    print("Playing file for keyword " + keyword + "...")
    play_audio_once(keyword_file_path)

def test():
    config = create_config()
    read_and_play("Human", config)