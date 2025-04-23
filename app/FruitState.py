# app/FruitState.py

from statistics import mean, median
from typing import List

import reflex as rx
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.db_models import Berries

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
        """Load berry entries from Postgres via SQLAlchemy."""
        session: Session = SessionLocal()
        try:
            records = session.query(Berries).all()
            self.items = [
                Berry(
                    bunch_id=str(r.bunch_id),
                    berry_id=str(r.id),
                    berry_size=float(r.axis_1),
                )
                for r in records
            ]
        finally:
            session.close()

    @rx.var(cache=True)
    def median_berry_size(self) -> float:
        sizes = [b.berry_size for b in self.items]
        return median(sizes) if sizes else 0.0

    @rx.var(cache=True)
    def average_berry_size(self) -> float:
        sizes = [b.berry_size for b in self.items]
        return mean(sizes) if sizes else 0.0
