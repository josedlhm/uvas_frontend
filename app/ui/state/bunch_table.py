from typing import Any, List
import reflex as rx
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Bunches


class BunchRow(rx.Base):
    """One grape-bunch entry for the table."""
    bunch_id: str
    n_visible_berries: int
    n_estimated_berries: float


class BunchTableState(rx.State):
    """State to load, sort, and paginate the bunch table via SQL."""

    # Data storage
    rows: List[BunchRow] = []

    # Sorting & pagination controls
    sort_value: str = ""
    sort_reverse: bool = False
    total_items: int = 0
    offset: int = 0
    limit: int = 12

    @rx.event
    def load_rows(self) -> None:
        """
        Load a page of bunch records from the database,
        applying optional sorting and pagination in SQL.
        """
        session: Session = SessionLocal()
        try:
            # 1) Base query
            q = session.query(Bunches)

            # 2) Apply sorting if present
            if self.sort_value:
                col = getattr(Bunches, self.sort_value, None)
                if col is not None:
                    order = desc(col) if self.sort_reverse else asc(col)
                    q = q.order_by(order)

            # 3) Total count for pagination
            self.total_items = q.count()

            # 4) Fetch only the current page
            records = (
                q
                .offset(self.offset)
                .limit(self.limit)
                .all()
            )

            # 5) Map ORM objects to view-models
            self.rows = [
                BunchRow(
                    bunch_id=str(r.id),
                    n_visible_berries=int(r.n_visible_berries or 0),
                    n_estimated_berries=float(r.n_estimated_berries or 0),
                )
                for r in records
            ]
        finally:
            session.close()

    @rx.var(cache=True)
    def total_pages(self) -> int:
        """Compute total pages based on count and limit."""
        if not self.total_items:
            return 1
        return (self.total_items + self.limit - 1) // self.limit

    @rx.var(cache=True)
    def page_number(self) -> int:
        """Compute 1-indexed current page number."""
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def current_page(self) -> List[Any]:
        """Return the last-loaded set of rows for display."""
        return self.rows

    @rx.event
    def set_sort_value(self, value: str) -> None:
        """
        Update the sort column, reset to first page, and reload.
        """
        self.sort_value = value
        self.offset = 0
        self.load_rows()

    @rx.event
    def toggle_sort(self) -> None:
        """
        Reverse sort direction and reload the current page.
        """
        self.sort_reverse = not self.sort_reverse
        self.load_rows()

    @rx.event
    def first_page(self) -> None:
        """Jump to the first page and reload."""
        self.offset = 0
        self.load_rows()

    @rx.event
    def prev_page(self) -> None:
        """Go to the previous page if possible, then reload."""
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_rows()

    @rx.event
    def next_page(self) -> None:
        """Go to the next page if possible, then reload."""
        if (self.offset + self.limit) < self.total_items:
            self.offset += self.limit
            self.load_rows()

    @rx.event
    def last_page(self) -> None:
        """Jump to the last page and reload."""
        self.offset = (self.total_pages - 1) * self.limit
        self.load_rows()
