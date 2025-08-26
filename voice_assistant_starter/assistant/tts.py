import pyttsx3
from .config import TTS_RATE, TTS_VOLUME

_engine = None

def init_tts():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', TTS_RATE)
        _engine.setProperty('volume', TTS_VOLUME)
    return _engine

def speak(text: str):
    eng = init_tts()
    eng.say(text)
    eng.runAndWait()
