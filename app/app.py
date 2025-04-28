# app/app.py
import reflex as rx
from app.ui import styles
from app.db.session import engine
from app.db.models import Base

# Ensure all tables are created in your Postgres DB:
Base.metadata.create_all(bind=engine)

# Create the Reflex app.
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)

from app.ui.pages import plant   # noqa: E402,F401
from app.ui.pages import fruit   # noqa: E402,F401