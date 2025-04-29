# app/ui/state/upload_data.py

from typing import List
from datetime import datetime
import reflex as rx
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Upload

class UploadDataRow(rx.Base):
    crop_type: str
    variety: str
    location: str
    day: str
    hour: str

class UploadDataState(rx.State):
    """State to load and format the list of uploads."""
    rows: List[UploadDataRow] = []

    @rx.event
    def load_upload_data(self) -> None:
        session: Session = SessionLocal()
        try:
            records = (
                session
                .query(Upload)
                .order_by(Upload.created_at.desc())
                .all()
            )
            self.rows = [
                UploadDataRow(
                    crop_type=getattr(r, "crop_type", ""),    # future column
                    variety=getattr(r, "variety", ""),        # future column
                    location=getattr(r, "location", ""),      # future column
                    day=r.created_at.strftime("%d-%m-%Y") if r.created_at else "",
                    hour=r.created_at.strftime("%H:%M:%S") if r.created_at else "",
                )
                for r in records
            ]
        finally:
            session.close()
