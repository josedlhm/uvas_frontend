import sqlite3
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
        """Load all bunches from the SQLite database (skip header)."""
        db_path = Path(__file__).parent.parent / "data" / "app.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bunch_id, n_visible_berries, n_estimated_berries
            FROM bunch_data
            WHERE bunch_id <> 'bunch_id'
        """)
        records = cursor.fetchall()
        conn.close()

        self.rows = [
            BunchRow(
                bunch_id=b,
                n_visible_berries=int(v),
                n_estimated_berries=float(e),
            )
            for b, v, e in records
        ]
        self.total_items = len(self.rows)

    @rx.var(cache=True)
    def filtered_rows(self) -> List[Any]:
        items = self.rows
        if self.sort_value:
            items = sorted(
                items,
                key=lambda r: getattr(r, self.sort_value),
                reverse=self.sort_reverse,
            )
        return items

    @rx.var(cache=True)
    def current_page(self) -> List[Any]:
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
