from __future__ import annotations
from typing import Any, List

import reflex as rx
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Berries
from app.ui.state.pagination import PaginationHelpers


class BerryRow(rx.Base):
    bunch_id: str
    berry_id: str
    berry_size: float


class BerryTableState(PaginationHelpers, rx.State):
    """State for the berry table (Fruit page)."""

    # unique client key
    state_name = "berry_table"

    # primitive fields -------------------------------------------------
    rows: List[Any] = []
    sort_value: str = ""
    sort_reverse: bool = False
    offset: int = 0
    limit: int = 12

    # -------- reactive vars -----------------------------------------
    @rx.var(cache=True)
    def filtered_rows(self) -> List[Any]:
        return self._filtered()

    @rx.var(cache=True)
    def current_page(self) -> List[Any]:
        return self._page()

    @rx.var(cache=True)
    def page_number(self) -> int:
        return self._page_num()

    @rx.var(cache=True)
    def total_items(self) -> int:
        return self._total_items()

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return self._total_pages()

    # -------- navigation events -------------------------------------
    toggle_sort    = rx.event(PaginationHelpers._toggle_sort)
    first_page     = rx.event(PaginationHelpers._first_page)
    prev_page      = rx.event(PaginationHelpers._prev_page)
    next_page      = rx.event(PaginationHelpers._next_page)
    last_page      = rx.event(PaginationHelpers._last_page)

    # -------- data loader -------------------------------------------
    @rx.event
    def load_rows(self):
        with SessionLocal() as db:
            self.rows = [
                BerryRow(
                    bunch_id=str(r.bunch_id),
                    berry_id=str(r.id),
                    berry_size=float(r.axis_1),
                )
                for r in db.query(Berries).all()
            ]
