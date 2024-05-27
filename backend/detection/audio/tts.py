import os
import torch
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import time
import pyaudio
import numpy as np
from . import spatial

AUDIO_CHUNK_SIZE = 1024


class TTS:
    def __init__(self):
        super().__init__()

        self.synthesiser = self.load_model()
        self.speaker_embedding = self.load_speaker()


    def speak(self, text, model, speaker_embedding):
        # synthesise speech with the speaker's embedding
        speech = model(text, forward_params={"speaker_embeddings": speaker_embedding})
        return speech

    # Passing speech audio directly yo PyAudio, do not need to create a new audio file
    def play_audio_once(self, speech):

        audio_np = np.squeeze(speech['audio'])

        p = pyaudio.PyAudio()  
        #open stream  
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=16000,
                        output=True) 
        # Play audio
        stream.write(audio_np.tobytes())

        # Close stream
        stream.stop_stream()
        stream.close()

        # Terminate PyAudio
        p.terminate()

    def generate_and_play(self, keyword):

        speech = self.speak(keyword, self.synthesiser, self.speaker_embedding)

        # plays the file corresponding to the keyword
        print("Playing file for keyword " + keyword + "...")
        self.play_audio_once(speech)

    def load_model(self):
        model = pipeline("text-to-speech", "microsoft/speecht5_tts")
        return model


    def load_speaker(self):
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
        return speaker_embedding

            

# def generate_and_play_spatial(keyword, config, x, y, spatial_config):
#     path = try_generate(keyword, config)

#     # plays the file corresponding to the keyword
#     print("Playing spatial file for keyword " + keyword + "...")
    
#     panned_audio_path = spatial.generate_spatial_audio(path, x, y, spatial_config)
#     play_audio_once(panned_audio_path)

#     # we remove the panned audio file after playing it, because it's coordinate specific
#     os.remove(panned_audio_path)
    

# def test():
#     tts_config = create_config()

#     keywords = ["Human", "Door", "Dog", "Bike", "Construction", "Car", "Cat", "Traintracks", "Puddle", "Fire"]
    
#     for keyword in keywords:
#         time.sleep(0.5)
#         generate_and_play(keyword, tts_config)

# def test_spatial():
#     MAX_X = 1000
#     MAX_VOLUME_PARANTHESES_MAYBE_Z_PARANTHESES = 1000

#     tts_config = create_config()
#     spatial_config = spatial.create_spatial_config(MAX_X, MAX_VOLUME_PARANTHESES_MAYBE_Z_PARANTHESES)

#     keywords = ["Human", "Door", "Dog", "Bike", "Construction", "Car", "Cat", "Traintracks", "Puddle", "Fire"]
    
#     i = 0
#     for keyword in keywords:
#         time.sleep(0.5)
        
#         generate_and_play_spatial(keyword, tts_config, MAX_X / len(keywords) * i, MAX_VOLUME_PARANTHESES_MAYBE_Z_PARANTHESES, spatial_config)
        
#         i += 1