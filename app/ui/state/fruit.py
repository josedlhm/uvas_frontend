# app/ui/state/fruit.py
from statistics import mean, median
from typing import Any, Dict, List, Optional

import reflex as rx
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Berries, Upload

class Berry(rx.Base):
    bunch_id: str
    berry_id: str
    berry_size: float

class FruitScanState(rx.State):
    items: List[Berry] = []
    upload_options: List[str] = []          # now strings
    filter_upload_id: Optional[str] = None  # holds the selected string

    @rx.event
    def load_upload_options(self) -> None:
        session: Session = SessionLocal()
        try:
            # get distinct upload IDs as ints, then stringify
            ids = session.query(Upload.id).distinct().all()
            self.upload_options = [str(u[0]) for u in ids]
        finally:
            session.close()

    @rx.event
    def set_filter_upload_id(self, upload_id: str) -> None:
        # '' means no filter
        self.filter_upload_id = upload_id 
        self.load_entries()

    @rx.event
    def load_entries(self) -> None:
        session: Session = SessionLocal()
        try:
            q = session.query(Berries)
            if self.filter_upload_id:
                q = q.filter(
                    Berries.upload_id == int(self.filter_upload_id)
                )
            records = q.all()
            self.items = [
                Berry(
                    bunch_id=str(r.bunch_id),
                    berry_id=str(r.id),
                    berry_size=float(r.axis_2),
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

    @rx.var(cache=True)
    def size_distribution(self) -> List[Dict[str, Any]]:
        sizes = [b.berry_size for b in self.items]
        if not sizes:
            return []
        min_s, max_s = min(sizes), max(sizes)
        width = (max_s - min_s) / 10 if max_s > min_s else 1
        bins = [0] * 10
        for s in sizes:
            idx = int((s - min_s) / width)
            if idx >= 10:
                idx = 9
            bins[idx] += 1
        data = []
        for i, count in enumerate(bins):
            edge = min_s + i * width
            data.append({"bin": f"{edge:.1f}", "count": count})
        return data
