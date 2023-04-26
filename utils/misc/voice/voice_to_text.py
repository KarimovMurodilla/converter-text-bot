import os
import speech_recognition as sr

from pathlib import Path


class Voice2Text:
    def __init__(self):
        self.__dir = Path(__file__).resolve().parent / 'voices'
    

    def convert(self, file_name, language):
        os.system(f"ffmpeg -y -i {self.__dir}/{file_name}.ogg {file_name}.wav")
        r = sr.Recognizer()
        file_audio = sr.AudioFile(f"{self.__dir}{file_name}.wav")

        with file_audio as source:
            audio_text = r.record(source)

        text = r.recognize_google(audio_text, language = language)

        return text
    

    def get_dir(self):
        return self.__dir