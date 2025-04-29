# app/ui/state/berry_table.py

from typing import Any, List
import reflex as rx
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Berries

class BerryRow(rx.Base):
    bunch_id: str
    berry_id: str
    berry_size: float

class BerryTableState(rx.State):
    """State to load & paginate the berry table via SQL."""

    rows: List[BerryRow] = []

    # sorting / pagination controls
    sort_value: str = ""
    sort_reverse: bool = False
    total_items: int = 0
    offset: int = 0
    limit: int = 12

    @rx.event
    def load_rows(self) -> None:
        session: Session = SessionLocal()
        try:
            q = session.query(Berries)

            # Apply sorting
            if self.sort_value:
                col = getattr(Berries, self.sort_value, None)
                if col is not None:
                    order = desc(col) if self.sort_reverse else asc(col)
                    q = q.order_by(order)

            # Total count for pagination
            self.total_items = q.count()

            # Fetch current page
            records = (
                q
                .offset(self.offset)
                .limit(self.limit)
                .all()
            )

            # Map to view-model
            self.rows = [
                BerryRow(
                    bunch_id=str(r.bunch_id),
                    berry_id=str(r.id),
                    berry_size=float(r.axis_1),
                )
                for r in records
            ]
        finally:
            session.close()

    @rx.var(cache=True)
    def total_pages(self) -> int:
        if not self.total_items:
            return 1
        return (self.total_items + self.limit - 1) // self.limit

    @rx.var(cache=True)
    def page_number(self) -> int:
        # Pages are 1-indexed
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def current_page(self) -> List[Any]:
        return self.rows

    # ── UI event handlers ────────────────────────────────────────────

    def toggle_sort(self) -> None:
        self.sort_reverse = not self.sort_reverse
        self.load_rows()

    def first_page(self) -> None:
        self.offset = 0
        self.load_rows()

    def prev_page(self) -> None:
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_rows()

    def next_page(self) -> None:
        if (self.offset + self.limit) < self.total_items:
            self.offset += self.limit
            self.load_rows()

    def last_page(self) -> None:
        self.offset = (self.total_pages - 1) * self.limit
        self.load_rows()
