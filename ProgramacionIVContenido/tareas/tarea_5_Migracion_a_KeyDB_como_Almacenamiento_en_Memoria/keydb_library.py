import json
from typing import Dict, Iterable, List, Optional

import redis

from book import Book


class BookNotFoundError(Exception):
    """Raised when a book is not found in the data store."""


class KeyDBLibrary:
    def __init__(self, *, host: str, port: int, password: Optional[str], db: int = 0) -> None:
        self._client = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True,
        )
        self._id_counter_key = "book:id"

    def _book_key(self, book_id: int) -> str:
        return f"book:{book_id}"

    def _load_book(self, key: str) -> Optional[Book]:
        raw_data = self._client.get(key)
        if raw_data is None:
            return None
        return Book.from_dict(json.loads(raw_data))

    def ping(self) -> bool:
        return self._client.ping()

    def add_book(self, book: Book) -> Book:
        book.id = int(self._client.incr(self._id_counter_key))
        self._client.set(self._book_key(book.id), json.dumps(book.to_dict()))
        return book

    def get_book(self, book_id: int) -> Book:
        book = self._load_book(self._book_key(book_id))
        if book is None:
            raise BookNotFoundError(f"No se encontró el libro con id {book_id}")
        return book

    def update_book(self, book_id: int, *, title: Optional[str] = None, author: Optional[str] = None, genre: Optional[str] = None, status: Optional[str] = None) -> Book:
        book = self.get_book(book_id)
        book.update(title=title, author=author, genre=genre, status=status)
        self._client.set(self._book_key(book.id), json.dumps(book.to_dict()))
        return book

    def delete_book(self, book_id: int) -> None:
        deleted = self._client.delete(self._book_key(book_id))
        if deleted == 0:
            raise BookNotFoundError(f"No se encontró el libro con id {book_id}")

    def list_books(self) -> List[Book]:
        return list(self._iter_books())

    def search_books(self, *, title: Optional[str] = None, author: Optional[str] = None, genre: Optional[str] = None) -> List[Book]:
        filters = {
            "title": title.lower() if title else None,
            "author": author.lower() if author else None,
            "genre": genre.lower() if genre else None,
        }
        results: List[Book] = []
        for book in self._iter_books():
            if self._matches_filters(book, filters):
                results.append(book)
        return results

    def _iter_books(self) -> Iterable[Book]:
        for key in self._client.scan_iter(match="book:*"):
            if key == self._id_counter_key:
                continue
            book = self._load_book(key)
            if book is not None:
                yield book

    def _matches_filters(self, book: Book, filters: Dict[str, Optional[str]]) -> bool:
        if filters["title"] and filters["title"] not in book.title.lower():
            return False
        if filters["author"] and filters["author"] not in book.author.lower():
            return False
        if filters["genre"] and filters["genre"] not in book.genre.lower():
            return False
        return True
