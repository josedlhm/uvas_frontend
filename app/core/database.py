from rxconfig import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Now this actually refers to the Config() you defined in rxconfig.py:
DATABASE_URL = config.db_url

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
