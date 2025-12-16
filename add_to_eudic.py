#!/usr/bin/env python

# API Reference: http://my.eudic.net/OpenAPI/doc_api_study

import argparse
import fileinput
import os
import sys

import requests


def words_generator(input):
    for line in input:
        if line.startswith("#"):
            continue
        word = line.split(":", maxsplit=1)[0].strip()
        if word != '':
            yield word

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="*")
    # Add the --book argument
    parser.add_argument("--book", help="Specify the book name")
    parser.add_argument(
        "--move", action="store_true", help="Remove from the default book"
    )

    # Parse the command line arguments
    args = parser.parse_args()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
        "Authorization": os.environ["EUDIC_TOKEN"],
    }

    if args.book is not None:
        books = requests.get(
            "https://api.frdic.com/api/open/v1/studylist/category?language=en",
            headers=headers,
        ).json()["data"]
        book_id = None
        for book in books:
            if book["name"] == args.book:
                book_id = book["id"]
                break
        if book_id is None:
            sys.stderr.write(f"Book not found: {args.book}\n")
            sys.exit(1)
    else:
        book_id = "0"

    words = list(words_generator(fileinput.input(args.file)))
    requests.post(
        "https://api.frdic.com/api/open/v1/studylist/words",
        headers=headers,
        json={"id": book_id, "language": "en", "words": words},
    )

    if book_id != "0" and args.move:
        requests.delete(
            "https://api.frdic.com/api/open/v1/studylist/words",
            headers=headers,
            json={"id": "0", "language": "en", "words": words},
        )
