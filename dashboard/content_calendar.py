from dataclasses import dataclass, field
from typing import List


@dataclass
class ContentCalendarItem:
    title: str
    date: str
    platform: str
    status: str = "planned"


class ContentCalendar:
    """Simple calendar model for planning weekly posts."""

    def __init__(self):
        self.items: List[ContentCalendarItem] = []

    def add_item(self, title: str, date: str, platform: str, status: str = "planned") -> None:
        self.items.append(
            ContentCalendarItem(title=title, date=date, platform=platform, status=status)
        )

    def get_items(self) -> List[ContentCalendarItem]:
        return self.items
