# app/PlantState.py

from statistics import median
from typing import List

import reflex as rx
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.db_models import Bunches

class Bunch(rx.Base):
    """One grape-bunch entry from the database."""
    bunch_id: str
    berries_count: float

class PlantScanState(rx.State):
    """State for loading & computing metrics on grape-bunch data."""
    items: List[Bunch] = []

    @rx.event
    def load_entries(self):
        """Load bunch stats from Postgres via SQLAlchemy."""
        session: Session = SessionLocal()
        try:
            records = session.query(Bunches).all()
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
