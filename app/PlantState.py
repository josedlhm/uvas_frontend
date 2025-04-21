import sqlite3
from pathlib import Path
from statistics import median
from typing import List

import reflex as rx

class Bunch(rx.Base):
    """One grape‑bunch entry from the database."""
    bunch_id: str
    berries_count: float

class PlantScanState(rx.State):
    """State for loading & computing metrics on grape‑bunch data."""
    items: List[Bunch] = []

    @rx.event
    def load_entries(self):
        """Load bunch stats from SQLite for plant KPIs (skip header)."""
        db_path = Path(__file__).parent.parent / "data" / "app.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT bunch_id, n_visible_berries "
            "FROM bunch_data "
            "WHERE bunch_id <> 'bunch_id'"
        )
        records = cursor.fetchall()
        conn.close()

        self.items = [
            Bunch(bunch_id=b, berries_count=float(v))
            for b, v in records
        ]

    @rx.var(cache=True)
    def total_bunches(self) -> int:
        return len(self.items)

    @rx.var(cache=True)
    def median_berries(self) -> float:
        counts = [b.berries_count for b in self.items]
        return median(counts) if counts else 0.0
