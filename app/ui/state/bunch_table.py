from __future__ import annotations
from typing import Any, List

import reflex as rx
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Bunches
from app.ui.state.pagination import PaginationHelpers


class BunchRow(rx.Base):
    bunch_id: str
    n_visible_berries: int
    n_estimated_berries: float


class BunchTableState(PaginationHelpers, rx.State):
    """State for the bunch table (Plant page)."""

    state_name = "bunch_table"

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
                BunchRow(
                    bunch_id=str(r.id),
                    n_visible_berries=int(r.n_visible_berries or 0),
                    n_estimated_berries=float(r.n_estimated_berries or 0),
                )
                for r in db.query(Bunches).all()
            ]
