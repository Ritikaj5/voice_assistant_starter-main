import re
from typing import Optional, Dict, Any
import dateparser

INTENTS = (
    "set_reminder",
    "get_weather",
    "get_news",
    "list_reminders",
    "delete_reminder",
    "help",
    "exit",
)

def parse(text: str) -> Dict[str, Any]:
    t = text.lower().strip()

    if any(k in t for k in ("exit", "quit", "bye", "goodbye", "stop")):
        return {"intent": "exit"}

    if "help" in t:
        return {"intent": "help"}

    if re.search(r"list .*reminder", t):
        return {"intent": "list_reminders"}

    # delete reminder by id or ordinal word/number
    m = re.search(r"(delete|remove) reminder (\w+)", t)
    if m:
        return {"intent": "delete_reminder", "rid": m.group(2)}

    # weather in CITY
    m = re.search(r"(weather|temperature).* in ([a-zA-Z\s]+)$", t)
    if m:
        city = m.group(2).strip()
        return {"intent": "get_weather", "city": city}

    if "weather" in t or "temperature" in t:
        return {"intent": "get_weather"}  # default city

    # news
    if any(k in t for k in ("news", "headlines")):
        return {"intent": "get_news"}

    # set reminder - several patterns
    # e.g., "remind me to drink water in 10 minutes"
    m = re.search(r"remind me to (.+?) (at|on|in) (.+)", t)
    if m:
        task = m.group(1).strip()
        when = m.group(3).strip()
        dt = dateparser.parse(when)
        if dt:
            return {"intent": "set_reminder", "when": dt, "text": task}

    # e.g., "set a reminder at 6 pm to call mom"
    m = re.search(r"set (a )?reminder (for|at|on|in) (.+?) to (.+)", t)
    if m:
        when = m.group(3).strip()
        task = m.group(4).strip()
        dt = dateparser.parse(when)
        if dt:
            return {"intent": "set_reminder", "when": dt, "text": task}

    # fallback: try to parse any time expression and treat rest as task
    m = re.search(r"(?:remind me|set (?:a )?reminder).*", t)
    if m:
        # Try to find a time phrase using dateparser search
        dt = dateparser.parse(t, settings={'PREFER_DATES_FROM': 'future'})
        if dt:
            # remove the time phrase might be hard; default generic text
            return {"intent": "set_reminder", "when": dt, "text": "your task"}

    # Unknown
    return {"intent": "help"}
