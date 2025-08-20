import urllib.parse
from typing import Generator

from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_DRIVER = settings.VISUAL_DB_DRIVER
DB_SERVER = settings.VISUAL_DB_SERVER
DB_PORT = settings.VISUAL_DB_PORT
DB_DATABASE = settings.VISUAL_DB_NAME
DB_USER = settings.VISUAL_DB_USER
DB_PASSWORD = settings.VISUAL_DB_PASSWORD

odbc_str = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER},{DB_PORT};"
    f"DATABASE={DB_DATABASE};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "TrustServerCertificate=yes;"
)

connection_string = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"

engine = create_engine(connection_string, fast_executemany=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
