from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import text
import datetime as dt

class Base(DeclarativeBase):
    pass

def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)
