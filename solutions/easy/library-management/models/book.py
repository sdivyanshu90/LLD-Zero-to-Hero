from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Book:
    isbn: str
    title: str
    author: str