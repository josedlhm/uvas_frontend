# app/state.py
import csv
from pathlib import Path
from statistics import median
from typing import List

import reflex as rx


class Bunch(rx.Base):
    """One grape‐bunch entry from the CSV."""
    bunch_id: str
    berries_count: float


class PlantScanState(rx.State):
    """State for loading & computing metrics on grape‐bunch CSV data."""

    # Holds all the Bunch objects after load_entries()
    items: List[Bunch] = []

    @rx.event
    def load_entries(self):
        """Read plant_scans.csv into self.items (and trigger a rerender)."""
        path = Path(__file__).parent.parent / "data" / "bunch_data.csv"
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Convert each row into a Bunch, casting berries_count to float
            self.items = [
                Bunch(
                    bunch_id=row["bunch_id"],
                    berries_count=float(row["berries_count"]),
                )
                for row in reader
            ]

    @rx.var(cache=True)
    def total_bunches(self) -> int:
        """Total number of bunches (= number of CSV rows)."""
        return len(self.items)

    @rx.var(cache=True)
    def median_berries(self) -> float:
        """Median berries_count across all bunches."""
        # statistics.median will raise if list is empty; handle as needed
        counts = [b.berries_count for b in self.items]
        return median(counts) if counts else 0.0
