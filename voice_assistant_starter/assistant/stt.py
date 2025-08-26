import speech_recognition as sr

recognizer = sr.Recognizer()

def listen_once(timeout: float = 5, phrase_time_limit: float = 8) -> str | None:
    """Capture a single utterance from the default microphone.
    Returns the recognized text (lowercased) or None.
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        text = recognizer.recognize_google(audio)
        return text.lower().strip()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        # Network or API error
        return None
