import sys
import requests
import sqlite3
from pathlib import Path
from urllib.parse import urlencode, quote_plus, quote
import json
from io import BytesIO

API_ENDPOINT = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{0}?'


def create_tables(conn):
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS words (
            word VARCHAR(255) PRIMARY KEY,
            explanation TEXT
        )
        """
    )

    conn.commit()
    c.close()


def make_tree(text):
    try:
        return etree.parse(BytesIO(text.encode('utf-8')))
    except:
        print("Fail to lookup word, the response is {}".format(
            text), file=sys.stderr)
        raise


class DictionaryApi:
    def __init__(self, api_key, cache_db_path: Path):
        query_string = urlencode({'key': api_key}, quote_via=quote_plus)
        self.api_endpoint = API_ENDPOINT + query_string
        self.cache_db = sqlite3.connect(cache_db_path)
        create_tables(self.cache_db)

    def lookup(self, word):
        if self.cache_db is None:
            return json.loads(self.lookup_without_cache(word))

        c = self.cache_db.cursor()
        c.execute('SELECT word, explanation FROM words WHERE word=?', (word,))
        result = c.fetchone()
        self.cache_db.commit()

        if result is not None:
            return json.loads(result[1])

        result = [word, self.lookup_without_cache(word)]
        parsed = json.loads(result[1])
        c.execute('INSERT INTO words(word, explanation) VALUES (?,?)', result)
        self.cache_db.commit()
        return parsed

    def lookup_without_cache(self, word):
        return requests.get(self.api_endpoint.format(quote(word))).text


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    api = DictionaryApi(os.environ['DICTIONARY_API_KEY'], "words.sqlite3")
    print(json.dumps(api.lookup('erstwhile')))