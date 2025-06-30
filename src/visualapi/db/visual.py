import os
import urllib.parse
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_DRIVER = os.getenv("VISUAL_DB_DRIVER")
DB_SERVER = os.getenv("VISUAL_DB_SERVER")
DB_PORT = os.getenv("VISUAL_DB_PORT", "1433")
DB_DATABASE = os.getenv("VISUAL_DB_NAME")
DB_USER = os.getenv("VISUAL_DB_USER")
DB_PASSWORD = os.getenv("VISUAL_DB_PASSWORD")

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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
