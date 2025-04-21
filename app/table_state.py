# app/table_state.py
import csv
from pathlib import Path
from typing import Any, List

import reflex as rx

class BunchRow(rx.Base):
    """One grape‑bunch entry for the table."""
    bunch_id: str
    n_visible_berries: int
    n_estimated_berries: float


class BunchTableState(rx.State):
    """State to load & paginate the bunch table."""
    rows: List[BunchRow] = []

    # sorting / pagination controls
    sort_value: str = ""
    sort_reverse: bool = False
    total_items: int = 0
    offset: int = 0
    limit: int = 12

    @rx.event
    def load_rows(self):
        """Load data/new_data.csv into self.rows and set total_items."""
        path = Path(__file__).parent.parent / "data" / "bunch_data.csv"
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = [
                BunchRow(
                    bunch_id=row["bunch_id"],
                    n_visible_berries=int(row["n_visible_berries"]),
                    n_estimated_berries=float(row["n_estimated_berries"]),
                )
                for row in reader
            ]
        self.rows = records
        self.total_items = len(records)

    @rx.var(cache=True)
    def filtered_rows(self) -> list[Any]:
        """Sort rows by the selected column."""
        items = self.rows
        if self.sort_value:
            items = sorted(
                items,
                key=lambda r: getattr(r, self.sort_value),
                reverse=self.sort_reverse,
            )
        return items

    @rx.var(cache=True)
    def current_page(self) -> list[Any]:
        """Slice out the current page of sorted rows."""
        start = self.offset
        return self.filtered_rows[start : start + self.limit]

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        if not self.total_items:
            return 1
        return (self.total_items + self.limit - 1) // self.limit

    # actions to flip sort or move pages
    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse

    def first_page(self):
        self.offset = 0

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit