from __future__ import annotations

from dataclasses import dataclass, field

from models.book_item import BookItem, BookItemStatus
from models.member import Member
from services.reservation_service import ReservationService


@dataclass(slots=True)
class Library:
    reservation_service: ReservationService = field(default_factory=ReservationService)
    members: dict[str, Member] = field(default_factory=dict, init=False)
    items_by_barcode: dict[str, BookItem] = field(default_factory=dict, init=False)
    items_by_isbn: dict[str, list[BookItem]] = field(default_factory=dict, init=False)

    def register_member(self, member: Member) -> None:
        self.members[member.member_id] = member

    def add_book_item(self, item: BookItem) -> None:
        self.items_by_barcode[item.barcode] = item
        self.items_by_isbn.setdefault(item.book.isbn, []).append(item)

    def checkout_book(self, isbn: str, member_id: str) -> str:
        self._get_member(member_id)
        for item in self.items_by_isbn.get(isbn, []):
            if item.status is BookItemStatus.AVAILABLE:
                item.checkout(member_id)
                return f"Checked out {item.barcode} to {member_id}"
        raise ValueError(f"No available copy for {isbn}")

    def reserve_book(self, isbn: str, member_id: str) -> str:
        member = self._get_member(member_id)
        items = self.items_by_isbn.get(isbn)
        if not items:
            raise ValueError(f"No book found for ISBN {isbn}")
        self.reservation_service.reserve(items[0].book, member)
        return f"Reserved {isbn} for {member_id}"

    def return_book(self, barcode: str) -> str:
        item = self.items_by_barcode.get(barcode)
        if item is None:
            raise ValueError(f"Unknown barcode {barcode}")

        item.return_to_library()
        notification = self.reservation_service.notify_next(item.book)
        if notification is None:
            return f"Returned {barcode}"
        return f"Returned {barcode}; {notification}"

    def _get_member(self, member_id: str) -> Member:
        member = self.members.get(member_id)
        if member is None:
            raise ValueError(f"Unknown member {member_id}")
        return member