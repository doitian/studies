#!/usr/bin/env python
import fileinput
import os
import sqlite3
from pathlib import Path

WORDS_FILE_NAME = 'kindle_vocabulary.txt'
VOCAB_DB_PATH = '/Volumes/Kindle/system/vocabulary/vocab.db'

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
    out_dir = root_path / 'out'
    out_dir.mkdir(exist_ok=True, parents=True)
    return out_dir / WORDS_FILE_NAME


def gen_kindle_vocabulary(root_path: Path):
    words_path = ensure_words_path(root_path)
    conn = sqlite3.connect(VOCAB_DB_PATH)
    c = conn.cursor()

    with open(words_path, "w") as of:
        for row in c.execute(QUERY_SQL):
            print("{0} :{1}".format(*row), file=of)

    c.execute(MARK_SQL)

    return words_path


if __name__ == '__main__':
    gen_kindle_vocabulary(Path(os.getcwd()))
