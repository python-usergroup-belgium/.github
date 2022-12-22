"""Utilities - parse Meetup RSS to get events info to be shown in GitHub profile."""
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from typing import Self
from xml.etree import ElementTree

import requests
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from loguru import logger


@dataclass
class Event:
    """Event information shown in profile."""

    title: str
    link: str
    date: datetime


class DescriptionParser(HTMLParser):
    """Parse the description HTML from string to get datetime object."""

    def __init__(self: Self, s: str) -> None:
        """Initialize object and feed string."""
        super().__init__()
        self._data: list[str] = []
        self._text = s
        self.feed(s)

    @staticmethod
    def _parse(s: str) -> datetime | None:
        """Parse date but return `None` in case of errors."""
        try:
            return parse(s)
        except ParserError as err:
            logger.debug(f"Parsing datetime error - returning `None` (error: `{err}`).")

    def get_datetime(self: Self) -> datetime | None:
        """Get the datetime object from first successful parse of `_data` items."""
        for s in reversed([s for s in self._data if s.strip()]):
            if (dt := self._parse(s)) and (not s.isnumeric()):
                return dt

    def handle_data(self: Self, data: str) -> None:
        """Append everything to `_data`."""
        self._data.append(data)


def item2event(item: ElementTree.Element) -> Event:
    """
    Parse XML item to an event.

    Event date's year is omitted - if published date is after event date,
     adjust the year.
    """
    dt = DescriptionParser(item.find("description").text).get_datetime()
    pub = parse(item.find("pubDate").text)
    return Event(
        title=item.find("title").text,
        link=item.find("guid").text,
        date=dt.replace(year=dt.year + 1) if dt < pub else dt,
    )


def xml2events(tree: ElementTree.Element) -> list[Event]:
    """Get list of events from Meetup RSS XML information."""
    return [item2event(item) for item in tree.findall("channel/item")]


def url2eventstr(url: str) -> str:
    """Get the events string for the profile from URL RSS information."""
    response = requests.get(url)
    events = sorted(
        [
            e
            for e in xml2events(ElementTree.fromstring(response.content))
            if e.date > datetime.now()
        ],
        key=lambda e: e.date,
    )
    eventstr = "\n".join(
        f"- [{e.date.strftime('%d/%m/%y (%a), at %H:%M')} - {e.title}]({e.link})"
        for e in events
    )
    return f"## Upcoming events\n\n{eventstr}"


# if __name__ == "__main__":
