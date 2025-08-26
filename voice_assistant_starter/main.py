import sys, time
from datetime import datetime
from dateutil import tz

from assistant import tts, stt
from assistant.weather import get_weather
from assistant.news import get_headlines
from assistant.reminders import ReminderManager
from assistant.nlu import parse
from assistant.config import DEFAULT_CITY

BEEP = "\a"  # console beep

def say_and_print(text: str):
    print(text)
    tts.speak(text)

def help_text():
    return (
        "Try things like: "
        "\n- 'remind me to stretch in 10 minutes'"
        "\n- 'set a reminder at 6 pm to call mom'"
        "\n- 'what's the weather in Kampala?'"
        "\n- 'read the news'"
        "\n- 'list reminders' or 'delete reminder <id>'"
        "\n- 'exit'"
    )

def handle_intent(intent: dict, rm: ReminderManager):
    name = intent.get("intent")

    if name == "exit":
        say_and_print("Goodbye!")
        sys.exit(0)

    if name == "help":
        say_and_print(help_text())
        return

    if name == "get_news":
        headlines = get_headlines(limit=5)
        if not headlines:
            say_and_print("I couldn't fetch the news right now.")
            return
        say_and_print("Here are today's top headlines:")
        for i, h in enumerate(headlines, 1):
            print(f"{i}. {h['title']} ({h['source']})")
            tts.speak(h["title"])
        return

    if name == "get_weather":
        city = intent.get("city") or DEFAULT_CITY
        w = get_weather(city)
        if not w:
            say_and_print(f"Sorry, I couldn't get the weather for {city}.")
            return
        txt = f"Current weather in {w['city']}, {w['country']}: {w['description']}, {w['temperature_c']}°C with winds {w['windspeed_kmh']} km/h."
        say_and_print(txt)
        return

    if name == "set_reminder":
        when = intent.get("when")
        text = intent.get("text") or "your task"
        if when is None:
            say_and_print("I couldn't figure out the time for that reminder.")
            return
        # Ensure timezone-aware in local time
        local = tz.tzlocal()
        if when.tzinfo is None:
            when = when.replace(tzinfo=local)
        rem = rm.add(when, text)
        say_and_print(f"Reminder set for {when.strftime('%Y-%m-%d %H:%M')} with id {rem.id}.")
        return

    if name == "list_reminders":
        items = rm.list()
        if not items:
            say_and_print("You have no reminders.")
            return
        say_and_print("Here are your reminders:")
        for r in items:
            print(f"- {r.id} at {r.when.strftime('%Y-%m-%d %H:%M')}: {r.text}")
        return

    if name == "delete_reminder":
        rid = intent.get("rid")
        if not rid:
            say_and_print("Please say the reminder id to delete.")
            return
        ok = rm.remove(rid)
        if ok:
            say_and_print(f"Deleted reminder {rid}.")
        else:
            say_and_print(f"I couldn't find a reminder with id {rid}.")
        return

    # Default
    say_and_print(help_text())

def main():
    tts.init_tts()
    rm = ReminderManager()
    print("Voice Assistant ready. Press Enter to speak, or type your command and press Enter.")
    say_and_print("Hello! I'm ready. Press Enter and speak your command after the beep.")
    while True:
        user_in = input(">> ").strip()
        if user_in:
            text = user_in.lower()
        else:
            # Voice input
            print(BEEP, end='', flush=True)
            try:
                text = stt.listen_once() or ""
            except Exception:
                print("Listening failed. You can type commands as a fallback.")
                text = ""
        if not text:
            print("Didn't catch that. Try again or type 'help'.")
            continue
        print(f"You said: {text}")
        intent = parse(text)
        handle_intent(intent, rm)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting. Bye!")
