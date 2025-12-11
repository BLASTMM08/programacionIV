"""Modelos de datos para la aplicación de biblioteca personal."""
from __future__ import annotations

from sqlalchemy import Column, Integer, String

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="pendiente")

    def __repr__(self) -> str:  # pragma: no cover - representación humana
        return f"<Book id={self.id} title={self.title!r} author={self.author!r}>"
