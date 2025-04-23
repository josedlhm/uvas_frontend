import reflex as rx

config = rx.Config(
    app_name="app",
    db_url="postgresql+psycopg2://pipeline:admin@localhost:5432/pipeline_db"
)
