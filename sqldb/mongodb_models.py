#!/usr/bin/env python3
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass

class Movie(Base):
    """SQLAlchemy Movie model representing a movie in the catalog"""
    __tablename__ = "movies"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    director: Mapped[str]
    year: Mapped[int]
    genre: Mapped[str]
    duration: Mapped[int | None]
    rating: Mapped[float | None]
    synopsis: Mapped[str | None]
    price: Mapped[float | None]
    is_watched: Mapped[bool] = mapped_column(default=False)



