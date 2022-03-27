from typing import List
import sqlite3
import re


class Book:
    def __init__(self, book_number: int, short_name: str, long_name: str, book_color: str,
                 is_present: bool = True, title: str = None, sorting_order: str = None):
        self.book_number_: int = int(book_number)
        self.short_name_: str = short_name
        self.long_name_: str = long_name
        self.book_color_: str = book_color
        self.is_present_: bool = bool(is_present)
        self.title_: str = title
        self.sorting_order_: int = int(sorting_order) if sorting_order else None

    def book_number(self) -> int:
        return self.book_number_

    def short_name(self) -> str:
        return self.short_name_

    def long_name(self) -> str:
        return self.long_name_

    def book_color(self) -> str:
        return self.book_color_

    def is_present(self) -> bool:
        return self.is_present_

    def title(self) -> str:
        return self.title_

    def sorting_order(self) -> int:
        return self.sorting_order_

    def __repr__(self):
        return f"Book({self.book_number_}, {self.short_name_}, {self.long_name_}, {self.book_color_})"


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
    def __init__(self, book_number: int, chapter: int, verse: int, text: str, strip_tags = False):
        self.book_number_: int = int(book_number)
        self.chapter_: int = int(chapter)
        self.verse_: int = int(verse)

        self.text_: str = text
        self.strip_tags_ = strip_tags
        if strip_tags:
            self.text_ = self.__strip_tags()

    def __strip_tags(self, text = None) -> str:
        if not text:
            text = self.text_

        text = re.sub("<[Smf]>([^<]+)</[Smf]>", "", text)
        text = re.sub("<[iJet]>([^<]+)</[iJet]>", "\\1", text)
        text = re.sub("<n>([^<]+)</n>", "[\\1]", text)

        text = text.replace("<br/>", "").replace("<pb/>", "")

        # Embedded subheadings aren't supported yet
        text = re.sub("<h>([^<]+)</h>", "", text)

        return text.strip()

    def strip_tags(self) -> bool:
        return self.strip_tags_

    def book_number(self) -> int:
        return self.book_number_

    def chapter(self) -> int:
        return self.chapter_

    def verse(self) -> int:
        return self.verse_

    def text(self, strip_tags=False) -> str:
        if strip_tags:
            return self.__strip_tags()
        return self.text_

    def __repr__(self) -> str:
        return f"[{self.book_number_}.{self.chapter_}:{self.verse_}] {self.text_}"


class Module:
    def __init__(self, filename):
        self.filename_ = filename

        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.books_ = None
        self.books_all_ = None
        self.verses_ = None

        self.info_ = None

    def __parse_books(self, filename) -> List[Book]:
        self.cursor.execute('SELECT * FROM books LIMIT 1')
        query_fields = [description[0] for description in self.cursor.description]
        self.cursor.execute(f"SELECT {', '.join(query_fields)} FROM books")

        result = []
        for row in self.cursor.fetchall():
            result.append(Book(**{key: row[key] for key in row.keys()}))

        return result


    def __parse_books_all(self, filename) -> List[Book]:
        self.cursor.execute('SELECT * FROM books LIMIT 1')
        query_fields = [description[0] for description in self.cursor.description]
        self.cursor.execute(f"SELECT {', '.join(query_fields)} FROM books_all")

        result = []
        for row in self.cursor.fetchall():
            result.append(Book(**{key: row[key] for key in row.keys()}))

        return result


    def __parse_info(self, filename) -> Info:
        self.cursor.execute("SELECT name, value FROM info")
        return Info(
            **{
                name: value for (name, value) in self.cursor.fetchall()
            }
        )


    def __parse_verses(self, filename, strip_tags = False) -> List[Verse]:
        self.cursor.execute("SELECT book_number, chapter, verse, text"
                    " FROM verses")
        
        result = []
        for row in self.cursor.fetchall():
            result.append(Verse(**{key: row[key] for key in row.keys()}, strip_tags = strip_tags))
        
        return result

    def filename(self) -> str:
        return self.filename_

    def info(self) -> Info:
        if self.info_:
            return self.info_
        self.info_ = self.__parse_info(self.filename_)
        return self.info_

    def books(self) -> List[Book]:
        if self.books_:
            return self.books_
        self.books_ = self.__parse_books(self.filename_)
        return self.books_

    def books_all(self) -> List[Book]:
        if self.books_all_:
            return self.books_all_
        self.books_all_ = self.__parse_books_all(self.filename_)
        return self.books_all_

    def verses(self, strip_tags = False) -> List[Verse]:
        if self.verses_ and self.verses_.strip_tags() == strip_tags:
            return self.verses_
        self.verses_ = self.__parse_verses(self.filename_, strip_tags)
        return self.verses_

    def strip_tags(self):
        verses = self.verses(strip_tags = True)

        for verse in verses:
            self.cursor.execute(f"UPDATE verses SET text = ? WHERE "
                         "book_number = ? AND chapter = ? AND verse = ?",
                         (verse.text(), verse.book_number(), verse.chapter(), verse.verse())
                        )
        self.connection.commit()

    def __del__(self):
        self.connection.close()
