import ssense_tts

keywords = ["Human", "Door", "Dog", "Bike", "Construction", "Car", "Cat", "Traintracks", "Puddle", "Fire"]

tts_config = ssense_tts.create_config()

for keyword in keywords:
    ssense_tts.read_and_play(keyword, tts_config)
