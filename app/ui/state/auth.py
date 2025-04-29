# app/ui/state/auth.py
from typing import Optional
import reflex as rx
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import User

class AuthState(rx.State):
    username: str = ""
    password: str = ""
    current_user: Optional[int] = None

    @rx.event
    def set_username(self, uname: str):
        self.username = uname

    @rx.event
    def set_password(self, pwd: str):
        self.password = pwd

    @rx.event
    def login(self):
        session: Session = SessionLocal()
        try:
            user = session.query(User).filter_by(username=self.username).first()
        finally:
            session.close()

        if user:
            # store the user’s id in state
            self.current_user = user.id
            # redirect to home
            return rx.redirect("/uploads")
        else:
            return rx.window_alert("Invalid username or password.")
