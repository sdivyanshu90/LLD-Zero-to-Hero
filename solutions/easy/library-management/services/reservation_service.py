from __future__ import annotations

from dataclasses import dataclass, field

from models.book import Book
from models.member import Member


@dataclass(slots=True)
class ReservationService:
    waitlists: dict[str, list[Member]] = field(default_factory=dict)

    def reserve(self, book: Book, member: Member) -> None:
        queue = self.waitlists.setdefault(book.isbn, [])
        if any(existing.member_id == member.member_id for existing in queue):
            raise ValueError(f"Member {member.member_id} already reserved {book.isbn}")
        queue.append(member)

    def notify_next(self, book: Book) -> str | None:
        queue = self.waitlists.get(book.isbn, [])
        if not queue:
            return None

        member = queue.pop(0)
        message = f"{book.title} is now available for member {member.member_id}"
        member.notify(message)
        if not queue:
            self.waitlists.pop(book.isbn, None)
        return message