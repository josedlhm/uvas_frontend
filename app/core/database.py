from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ── STEP 1a: set this to the absolute path where your pipeline writes pipeline_data.db
SQLITE_PATH = "/full/path/to/your/pipeline/repo/pipeline_data.db"
DATABASE_URL = f"sqlite:///{SQLITE_PATH}"

# no concurrent‑write safety needed for now
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
