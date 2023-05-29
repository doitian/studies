#!/usr/bin/env python
import os
import fileinput
import requests


def words_generator(input):
    for line in input:
        if line.startswith('#'):
            continue
        yield line.split(':', maxsplit=1)[0].strip()


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    words = list(words_generator(fileinput.input()))
    requests.post(
        "https://api.frdic.com/api/open/v1/studylist/words",
        headers={
            "Authorization": os.environ['EUDIC_TOKEN']
        },
        json={
            "id": "0",
            "language": "en",
            "words": words
        })