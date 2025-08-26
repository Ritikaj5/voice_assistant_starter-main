# Voice-Activated Personal Assistant (Starter Project)

Python voice assistant that can:
- Set reminders (spoken or typed) and speak them at the right time
- Check current weather by city (uses Open‑Meteo: no API key needed)
- Read the latest news headlines (RSS feeds: no API key needed)
- Listen with your microphone (SpeechRecognition + PyAudio)
- Talk back to you (pyttsx3 text‑to‑speech)

## Quick Start

```bash
# 1) Create a virtual environment (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# (macOS) If PyAudio fails, first: brew install portaudio
# (Linux)   If PyAudio fails, first: sudo apt-get install portaudio19-dev python3-pyaudio

# 3) (Optional) configure defaults
cp .env.example .env  # then edit .env

# 4) Run
python main.py
```

## Voice Commands (examples)

- "remind me to stretch in 10 minutes"
- "set a reminder at 6 pm to call mom"
- "what's the weather in Delhi?"
- "read the news" / "headlines"
- "list reminders" / "delete reminder one"
- "help" / "exit"

Press **Enter** to start listening; speak your command after the beep.
You can also **type** a command and press Enter.

## Notes

- Reminders persist in `data/reminders.json`.
- Weather: Open‑Meteo current weather (no key required).
- News: parses a few RSS feeds (BBC, Reuters, AP). Change them in `assistant/news.py`.
