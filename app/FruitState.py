import sqlite3
from pathlib import Path
from statistics import mean, median
from typing import List

import reflex as rx

class Berry(rx.Base):
    """One berry entry from the database."""
    bunch_id: str
    berry_id: str
    berry_size: float

class FruitScanState(rx.State):
    """State for loading & computing metrics on berry data."""
    items: List[Berry] = []

    @rx.event
    def load_entries(self):
        """Load berry entries from SQLite for stats (skip header)."""
        db_path = Path(__file__).parent.parent / "data" / "app.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT bunch_id, berry_id, berry_size "
            "FROM berry_data "
            "WHERE bunch_id <> 'bunch_id'"
        )
        records = cursor.fetchall()
        conn.close()

        self.items = [
            Berry(bunch_id=b, berry_id=i, berry_size=float(s))
            for b, i, s in records
        ]

    @rx.var(cache=True)
    def median_berry_size(self) -> float:
        sizes = [b.berry_size for b in self.items]
        return median(sizes) if sizes else 0.0

    @rx.var(cache=True)
    def average_berry_size(self) -> float:
        sizes = [b.berry_size for b in self.items]
        return mean(sizes) if sizes else 0.0
