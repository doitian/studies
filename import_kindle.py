#!/usr/bin/env python
"""
Add new words from Kindle vocabulary database to words.txt.
Appends words in the format: word: example sentence
"""

import os
import sqlite3
import sys

VOCAB_DB_PATH = "D:/system/vocabulary/vocab.db"
# '/Volumes/Kindle/system/vocabulary/vocab.db'

WORDS_FILE = "words.txt"

QUERY_SQL = """
SELECT WORDS.stem, LOOKUPS.usage || ' — ' || BOOK_INFO.title
FROM WORDS
       LEFT JOIN LOOKUPS ON WORDS.id = LOOKUPS.word_key
       LEFT JOIN BOOK_INFO ON LOOKUPS.book_key = BOOK_INFO.id
WHERE WORDS.category = 0
"""

MARK_SQL = """
UPDATE WORDS SET category = 100
WHERE category = 0
"""


def import_kindle():
    """Add new words from Kindle to words.txt."""
    if not os.path.exists(VOCAB_DB_PATH):
        print(f"Error: Kindle vocabulary database not found at {VOCAB_DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(VOCAB_DB_PATH)
    c = conn.cursor()

    words_to_add = []
    for row in c.execute(QUERY_SQL):
        words_to_add.append(row)

    if not words_to_add:
        print("No new words found in Kindle vocabulary database.")
        conn.close()
        return

    print(f"Found {len(words_to_add)} new words to add to {WORDS_FILE}...")

    successful = 0
    failed = 0

    try:
        with open(WORDS_FILE, "a", encoding="utf-8") as f:
            for word, example in words_to_add:
                try:
                    # Format: word: example
                    f.write(f"{word}: {example}\n")
                    print(f"✓ Added '{word}' to {WORDS_FILE}")
                    successful += 1
                except Exception as e:
                    print(f"✗ Error adding '{word}': {e}", file=sys.stderr)
                    print(f"  {example}", file=sys.stderr)
                    failed += 1
    except Exception as e:
        print(f"✗ Error opening {WORDS_FILE}: {e}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    print(f"\nSummary: {successful} successful, {failed} failed")

    if failed == 0:
        # Mark successfully added words as processed
        conn.execute(MARK_SQL)
        conn.commit()
        print(f"Marked {successful} words as processed in Kindle database.")

    conn.close()


if __name__ == "__main__":
    import_kindle()

