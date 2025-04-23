# app/app.py
import reflex as rx
from . import styles
from app.core.database import engine
from app.models.db_models import Base

# Ensure all tables are created in your Postgres DB:
Base.metadata.create_all(bind=engine)

# Create the Reflex app.
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)
