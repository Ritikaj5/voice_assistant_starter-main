from __future__ import annotations
import json, os, uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from dateutil import tz

from . import tts
from .config import REMINDERS_DB

@dataclass
class Reminder:
    id: str
    when_iso: str  # ISO time in local timezone
    text: str

    @property
    def when(self) -> datetime:
        return datetime.fromisoformat(self.when_iso)

class ReminderManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.reminders: List[Reminder] = []
        self.load()

    def _announce(self, text: str):
        tts.speak(f"Reminder: {text}")

    def add(self, when: datetime, text: str) -> Reminder:
        rid = str(uuid.uuid4())[:8]
        rem = Reminder(id=rid, when_iso=when.isoformat(), text=text)
        self.reminders.append(rem)
        self._schedule(rem)
        self.save()
        return rem

    def _schedule(self, rem: Reminder):
        trigger = DateTrigger(run_date=rem.when)
        self.scheduler.add_job(lambda: self._announce(rem.text), trigger=trigger, id=rem.id, replace_existing=True)

    def list(self) -> List[Reminder]:
        return list(self.reminders)

    def remove(self, rid: str) -> bool:
        for i, r in enumerate(self.reminders):
            if r.id == rid:
                self.reminders.pop(i)
                try:
                    self.scheduler.remove_job(r.id)
                except Exception:
                    pass
                self.save()
                return True
        return False

    def save(self):
        os.makedirs(os.path.dirname(REMINDERS_DB), exist_ok=True)
        with open(REMINDERS_DB, "w", encoding="utf-8") as f:
            json.dump([asdict(r) for r in self.reminders], f, indent=2)

    def load(self):
        if not os.path.exists(REMINDERS_DB):
            return
        try:
            with open(REMINDERS_DB, "r", encoding="utf-8") as f:
                items = json.load(f)
                self.reminders = [Reminder(**it) for it in items]
            # Reschedule future reminders
            from datetime import datetime, timezone
            now = datetime.now(tz.tzlocal())
            for r in self.reminders:
                if r.when > now:
                    self._schedule(r)
        except Exception:
            self.reminders = []
