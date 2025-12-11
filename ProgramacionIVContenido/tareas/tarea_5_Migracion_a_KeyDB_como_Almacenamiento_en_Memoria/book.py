from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Book:
    """Data representation of a library book."""

    id: Optional[int] = field(default=None)
    title: str = field(default="")
    author: str = field(default="")
    genre: str = field(default="")
    status: str = field(default="")

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Book":
        return cls(
            id=int(data.get("id")) if data.get("id") is not None else None,
            title=data.get("title", ""),
            author=data.get("author", ""),
            genre=data.get("genre", ""),
            status=data.get("status", ""),
        )

    def update(self, **changes: str) -> None:
        for field_name, value in changes.items():
            if hasattr(self, field_name) and value is not None:
                setattr(self, field_name, value)
