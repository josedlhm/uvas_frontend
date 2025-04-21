import csv
from pathlib import Path
from statistics import mean, median
from typing import List

import reflex as rx

class Berry(rx.Base):
    """One berry entry from the CSV."""
    bunch_id: str
    berry_id: str
    berry_size: float

class FruitScanState(rx.State):
    """State for loading & computing metrics on berry CSV data."""
    items: List[Berry] = []

    @rx.event
    def load_entries(self):
        """Read berry_data.csv into self.items (and trigger a rerender)."""
        path = Path(__file__).parent.parent / "data" / "berry_data.csv"
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.items = [
                Berry(
                    bunch_id=row["bunch_id"],
                    berry_id=row["berry_id"],
                    berry_size=float(row["berry_size"]),
                )
                for row in reader
            ]

    @rx.var(cache=True)
    def median_berry_size(self) -> float:
        """Median berry_size across all berries."""
        sizes = [b.berry_size for b in self.items]
        return median(sizes) if sizes else 0.0

    @rx.var(cache=True)
    def average_berry_size(self) -> float:
        """Average berry_size across all berries."""
        sizes = [b.berry_size for b in self.items]
        return mean(sizes) if sizes else 0.0
