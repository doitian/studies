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
        yield line.split(":", maxsplit=1)[0].strip()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="*")
    # Add the --book argument
    parser.add_argument("--book", help="Specify the book name")

    # Parse the command line arguments
    args = parser.parse_args()

    if args.book is not None:
        books = requests.get(
            "https://api.frdic.com/api/open/v1/studylist/category?language=en",
            headers={"Authorization": os.environ["EUDIC_TOKEN"]},
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
        headers={"Authorization": os.environ["EUDIC_TOKEN"]},
        json={"id": book_id, "language": "en", "words": words},
    )
