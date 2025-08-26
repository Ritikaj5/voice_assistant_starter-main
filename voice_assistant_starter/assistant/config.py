import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

DEFAULT_CITY = os.getenv("DEFAULT_CITY", "delhi")
TTS_RATE = int(float(os.getenv("TTS_RATE", "180")))
TTS_VOLUME = float(os.getenv("TTS_VOLUME", "1.0"))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

REMINDERS_DB = os.path.join(DATA_DIR, "reminders.json")
