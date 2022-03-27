from typing import List
import sqlite3


class Book:
    def __init__(self, book_number, short_name, long_name, book_color):
        self.book_number = book_number
        self.short_name = short_name
        self.long_name = long_name
        self.book_color = book_color

    def __repr__(self):
        return f"Book({self.book_number}, {self.short_name}, {self.long_name}, {self.book_color})"


def parse_books(filename) -> List[Book]:
    con = sqlite3.connect(filename)
    cur = con.cursor()

    result = []
    cur.execute("SELECT book_number, short_name, long_name, book_color"
                " FROM books")
    for (book_number, short_name, long_name, book_color) in cur.fetchall():
        result.append(Book(book_number, short_name, long_name, book_color))

    return result
