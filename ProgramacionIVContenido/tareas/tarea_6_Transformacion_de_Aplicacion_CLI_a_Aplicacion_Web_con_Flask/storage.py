import uuid
from dataclasses import dataclass, asdict
from typing import List, Optional

from redis import Redis


@dataclass
class Book:
    id: str
    titulo: str
    autor: str
    genero: str
    estado: str

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            id=data.get("id", ""),
            titulo=data.get("titulo", ""),
            autor=data.get("autor", ""),
            genero=data.get("genero", ""),
            estado=data.get("estado", ""),
        )


class BookRepository:
    def __init__(self, client: Redis, prefix: str = "libro") -> None:
        self.client = client
        self.prefix = prefix

    def _key(self, book_id: str) -> str:
        return f"{self.prefix}:{book_id}"

    def create(self, titulo: str, autor: str, genero: str, estado: str) -> Book:
        book_id = str(uuid.uuid4())
        book = Book(id=book_id, titulo=titulo, autor=autor, genero=genero, estado=estado)
        self.client.hset(self._key(book_id), mapping=asdict(book))
        return book

    def all(self) -> List[Book]:
        books: List[Book] = []
        for key in self.client.scan_iter(match=f"{self.prefix}:*"):
            data = self.client.hgetall(key)
            decoded = {k.decode(): v.decode() for k, v in data.items()}
            books.append(Book.from_dict(decoded))
        books.sort(key=lambda book: book.titulo.lower())
        return books

    def get(self, book_id: str) -> Optional[Book]:
        data = self.client.hgetall(self._key(book_id))
        if not data:
            return None
        decoded = {k.decode(): v.decode() for k, v in data.items()}
        return Book.from_dict(decoded)

    def update(self, book_id: str, titulo: str, autor: str, genero: str, estado: str) -> Optional[Book]:
        if not self.client.exists(self._key(book_id)):
            return None
        book = Book(id=book_id, titulo=titulo, autor=autor, genero=genero, estado=estado)
        self.client.hset(self._key(book_id), mapping=asdict(book))
        return book

    def delete(self, book_id: str) -> bool:
        return bool(self.client.delete(self._key(book_id)))

    def search(self, query: str) -> List[Book]:
        normalized = query.lower().strip()
        if not normalized:
            return self.all()
        results = []
        for book in self.all():
            if (
                normalized in book.titulo.lower()
                or normalized in book.autor.lower()
                or normalized in book.genero.lower()
            ):
                results.append(book)
        return results
