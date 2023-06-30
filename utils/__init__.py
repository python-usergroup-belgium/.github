"""Utilities - parse Meetup API to get events info to be shown in GitHub profile."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests


@dataclass
class Event:
    """Event information shown."""

    name: str
    link: str
    date: datetime
    is_online_event: bool
    yes_rsvp_count: int
    city: str


def resp2event(d: dict[str, Any]) -> Event:
    """Create `Event` from API response."""
    return Event(
        name=d["name"],
        link=d["link"],
        date=datetime.strptime(
            f"{d['local_date']} {d['local_time']}", "%Y-%m-%d %H:%M"
        ),
        is_online_event=d["is_online_event"],
        city=d.get("venue", {}).get("city", "Everywhere"),
        yes_rsvp_count=d["yes_rsvp_count"],
    )


def url2eventstr(url: str) -> str:
    """Get the events string from API information."""
    response = requests.get(url)
    events = [resp2event(d) for d in response.json()]
    eventstr = "\n".join(
        f"- [{e.date.strftime('%d/%B/%Y (%a), %H:%M')} - {e.name}"
        f" @{e.city}{'💻' if e.is_online_event else ''}"
        f" ({e.yes_rsvp_count} 💁‍♀️💁‍♂️)]({e.link})"
        for e in events
    )
    _placeholder = (
        "👉 Join us at [Python User Group Belgium]"
        "(https://www.meetup.com/python-user-group-belgium/)"
        " to stay up to date with the latest events!"
    )
    return f"## Upcoming events\n\n{eventstr or _placeholder}"


def url2intro(url: str) -> str:
    """Get the events string from API information."""
    response = requests.get(url)
    return response.json()["description"]
