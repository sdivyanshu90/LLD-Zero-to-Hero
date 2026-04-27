from models.book import Book
from models.book_item import BookItem
from models.member import Member
from services.library import Library


def main() -> None:
    library = Library()
    member_a = Member(member_id="M1", name="Asha")
    member_b = Member(member_id="M2", name="Ravi")

    library.register_member(member_a)
    library.register_member(member_b)

    book = Book(isbn="ISBN-123", title="Designing Systems", author="S. Author")
    item = BookItem(barcode="COPY-1", book=book)
    library.add_book_item(item)

    print(library.checkout_book("ISBN-123", "M1"))
    print(library.reserve_book("ISBN-123", "M2"))
    print(library.return_book("COPY-1"))
    print(member_b.notifications)


if __name__ == "__main__":
    main()