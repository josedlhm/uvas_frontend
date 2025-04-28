# app/ui/state/pagination_helpers.py
from __future__ import annotations
from typing import Any, List

class PaginationHelpers:
    """Utility functions and nav logic (no reactive vars, no rx.State)."""

    # ---------- helpers that expect self.rows, self.offset, self.limit -----
    def _filtered(self) -> List[Any]:
        if not self.sort_value:
            return self.rows
        return sorted(
            self.rows,
            key=lambda r: getattr(r, self.sort_value),
            reverse=self.sort_reverse,
        )

    def _page(self) -> List[Any]:
        start = self.offset
        return self._filtered()[start : start + self.limit]

    def _page_num(self) -> int:
        return (self.offset // self.limit) + 1

    def _total_items(self) -> int:
        return len(self.rows)

    def _total_pages(self) -> int:
        return max(1, (self._total_items() + self.limit - 1) // self.limit)

    # ---------- nav helpers (not @rx.event yet) ----------------------------
    def _toggle_sort(self):
        self.sort_reverse = not self.sort_reverse

    def _first_page(self):
        self.offset = 0

    def _prev_page(self):
        if self._page_num() > 1:
            self.offset -= self.limit

    def _next_page(self):
        if self._page_num() < self._total_pages():
            self.offset += self.limit

    def _last_page(self):
        self.offset = (self._total_pages() - 1) * self.limit
