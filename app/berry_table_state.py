# app/berry_table_state.py

from typing import Any, List

import reflex as rx
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.db_models import Berries

class BerryRow(rx.Base):
    """One berry entry for the table."""
    bunch_id: str
    berry_id: str
    berry_size: float

class BerryTableState(rx.State):
    """State to load & paginate the berry table."""
    rows: List[BerryRow] = []

    # sorting / pagination controls
    sort_value: str = ""
    sort_reverse: bool = False
    total_items: int = 0
    offset: int = 0
    limit: int = 12

    @rx.event
    def load_rows(self):
        """Load all berries from Postgres via SQLAlchemy."""
        session: Session = SessionLocal()
        try:
            berries = session.query(Berries).all()
            self.rows = [
                BerryRow(
                    bunch_id=str(b.bunch_id),
                    berry_id=str(b.id),
                    berry_size=float(b.axis_1),
                )
                for b in berries
            ]
            self.total_items = len(self.rows)
        finally:
            session.close()

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
