#!/usr/bin/env python
import os
import sqlite3
from pathlib import Path

VOCAB_DB_PATH = "D:/system/vocabulary/vocab.db"
# '/Volumes/Kindle/system/vocabulary/vocab.db'

QUERY_SQL = """
SELECT WORDS.stem, LOOKUPS.usage || ' — ' || BOOK_INFO.title
FROM WORDS
       LEFT JOIN LOOKUPS ON WORDS.id = LOOKUPS.word_key
       LEFT JOIN BOOK_INFO ON LOOKUPS.book_key = BOOK_INFO.id
WHERE WORDS.category = 0
"""

MARK_SQL = """
UPDATE WORDS SET category = 100
"""


def ensure_words_path(root_path: Path):
    root_path.mkdir(exist_ok=True, parents=True)
    return root_path / "words.txt"


def gen_kindle_vocabulary(root_path: Path):
    words_path = ensure_words_path(root_path)
    conn = sqlite3.connect(VOCAB_DB_PATH)
    c = conn.cursor()

    with open(words_path, "a") as of:
        for row in c.execute(QUERY_SQL):
            print("{0} :{1}".format(*row), file=of)

    conn.execute(MARK_SQL)
    conn.commit()

    return words_path


if __name__ == "__main__":
    gen_kindle_vocabulary(Path(os.getcwd()))
