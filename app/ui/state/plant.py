# app/ui/state/plant.py

from statistics import median
from typing import Any, List

import reflex as rx
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import SessionLocal
from app.db.models import Bunches, Upload

class Bunch(rx.Base):
    """One grape-bunch entry from the database."""
    bunch_id: str
    berries_count: float

class PlantScanState(rx.State):
    """State for loading, filtering, and computing metrics on grape-bunch data."""
    items: List[Bunch] = []
    upload_options: List[str] = []   # distinct upload IDs, newest first
    filter_upload_id: str = ""       # currently selected upload

    @rx.event
    def load_upload_options(self) -> None:
        """Fetch distinct upload IDs (descending) and default to the newest."""
        session: Session = SessionLocal()
        try:
            rows = (
                session
                .query(Upload.id)
                .order_by(desc(Upload.id))
                .distinct()
                .all()
            )
            opts = [str(r[0]) for r in rows]
            self.upload_options = opts
            if opts:
                self.filter_upload_id = opts[0]
        finally:
            session.close()

    @rx.event
    def set_filter_upload_id(self, upload_id: str) -> None:
        """Update which upload to show and reload entries."""
        self.filter_upload_id = upload_id
        self.load_entries()

    @rx.event
    def load_entries(self) -> None:
        """Load bunch stats, filtered by the selected upload_id."""
        session: Session = SessionLocal()
        try:
            q = session.query(Bunches)
            if self.filter_upload_id:
                q = q.filter(Bunches.upload_id == int(self.filter_upload_id))
            records = q.all()
            self.items = [
                Bunch(
                    bunch_id=str(r.id),
                    berries_count=float(r.n_visible_berries or 0),
                )
                for r in records
            ]
        finally:
            session.close()

    @rx.var(cache=True)
    def total_bunches(self) -> int:
        return len(self.items)

    @rx.var(cache=True)
    def median_berries(self) -> float:
        counts = [b.berries_count for b in self.items]
        return median(counts) if counts else 0.0
