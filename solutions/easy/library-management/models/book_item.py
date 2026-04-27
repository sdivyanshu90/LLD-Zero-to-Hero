from dataclasses import dataclass
from enum import Enum

from .book import Book


class BookItemStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


@dataclass(slots=True)
class BookItem:
    barcode: str
    book: Book
    status: BookItemStatus = BookItemStatus.AVAILABLE
    borrowed_by: str | None = None

    def checkout(self, member_id: str) -> None:
        if self.status is not BookItemStatus.AVAILABLE:
            raise ValueError(f"Copy {self.barcode} is not available")
        self.status = BookItemStatus.BORROWED
        self.borrowed_by = member_id

    def return_to_library(self) -> None:
        self.status = BookItemStatus.AVAILABLE
        self.borrowed_by = None