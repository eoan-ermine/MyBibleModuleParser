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


class Info:
    def __init__(self, **kwargs):
        self.configuration = kwargs

    def chapter_string(self):
        return self.configuration.get("chapter_string", None)

    def chapter_string_ot(self):
        return self.configuration.get("chapter_string_ot", None)

    def chapter_string_nt(self):
        return self.configuration.get("chapter_string_nt", None)

    def chapter_string_ps(self):
        return self.configuration.get("chapter_string_ps", None)

    def introduction_string(self):
        return self.configuration.get("introduction_string", None)

    def strong_numbers(self):
        return self.configuration.get("strong_numbers", None)

    def right_to_left(self):
        return self.configuration.get("right_to_left", None)

    def right_to_left_ot(self):
        return self.configuration.get("right_to_left_ot", None)

    def right_to_left_nt(self):
        return self.configuration.get("right_to_left_nt", None)

    def book_list_right_to_left(self):
        return self.configuration.get("book_list_right_to_left", None)

    def book_list_right_to_left_ot(self):
        return self.configuration.get("book_list_right_to_left_ot", None)

    def book_list_right_to_left_nt(self):
        return self.configuration.get("book_list_right_to_left_nt", None)

    def digits09(self):
        return self.configuration.get("digits0-9", None)

    def font_scale(self):
        return self.configuration.get("font_scale", None)

    def strong_numbers_prefix(self):
        return self.configuration.get("strong_numbers_prefix", None)

    def contains_accents(self):
        return self.configuration.get("contains_accents", None)

    def add_space_before_footnote_marker(self):
        return self.configuration.get("add_space_before_footnote_marker", None)

    def associated_theme(self):
        return self.configuration.get("associated_theme", None)

    def morphology_topic_reference(self, language=None):
        return self.configuration.get("morphology_topic_reference" + ("_" + language) if language else "", None)

    def __repr__(self):
        return self.configuration.__repr__()


class Verse:
    def __init__(self, book_number, chapter, text):
        self.book_number = book_number
        self.chapter = chapter
        self.text = text

    def book_number(self):
        return self.book_number

    def chapter(self):
        return self.chapter

    def text(self):
        return self.text


def parse_books(filename) -> List[Book]:
    con = sqlite3.connect(filename)
    cur = con.cursor()

    result = []
    cur.execute("SELECT book_number, short_name, long_name, book_color"
                " FROM books")
    for (book_number, short_name, long_name, book_color) in cur.fetchall():
        result.append(Book(book_number, short_name, long_name, book_color))

    return result


def parse_books_all(filename) -> List[Book]:
    con = sqlite3.connect(filename)
    cur = con.cursor()

    result = []
    cur.execute("SELECT book_number, short_name, long_name, book_color"
                " FROM books_all")
    for (book_number, short_name, long_name, book_color) in cur.fetchall():
        result.append(Book(book_number, short_name, long_name, book_color))
    
    return result


def parse_info(filename) -> Info:
    con = sqlite3.connect(filename)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("SELECT name, value FROM info")
    return Info(
        **{
            name: value for (name, value) in cur.fetchall()
        }
    )


def parse_verses(filename) -> List[Verse]:
    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute("SELECT book_number, chapter, verse, text"
                " FROM verses")
    
    result = []
    for (book_number, chapter, verse, text) in cur.fetchall():
        result.append(Verse(book_number, chapter, verse, text))
    
    return result
