#!/usr/bin/env python
import sys
import os
import re
import csv
import dictionaryapi
import requests
import shutil
from pathlib import Path

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))

ALPHABET = re.compile(r"[a-zA-Z]")


def download_file(url):
    local_filename = url.split('/')[-1]
    out_dir = Path(os.getcwd()) / 'out' / 'audio'
    out_dir.mkdir(exist_ok=True)
    with requests.get(url, stream=True) as r:
        with open(out_dir / local_filename, 'wb') as f:
            print("save {}".format(out_dir / local_filename))
            shutil.copyfileobj(r.raw, f)

# An audio reference URL should be in the following form: https://media.merriam-webster.com/soundc11/[subdirectory]/[base filename].wav where [base filename] equals the value of audio, and [subdirectory] is determined as follows:
# •	if audio begins with "bix", the subdirectory should be "bix",
# •	if audio begins with "gg", the subdirectory should be "gg",
# •	if audio begins with a number or punctuation (eg, "_"), the subdirectory should be "number",
# •	otherwise, the subdirectory is equal to the first letter of audio.
# For example, the URL for the object {"audio":"3d000001","ref":"c","stat":"1"} in the entry "3-D" would be: https://media.merriam-webster.com/soundc11/number/3d000001.wav


def subdirectory_of(filename):
    if filename.startswith("bix"):
        return "bix"
    elif filename.startswith("gg"):
        return "gg"

    match = ALPHABET.match(filename)
    if match is not None:
        return match.group(0)
    return "number"


def pr_url(filename):
    return "https://media.merriam-webster.com/soundc11/{}/{}.wav".format(subdirectory_of(filename), filename)


def lookup_audio(root_dir: Path, word, download):
    api_client = dictionaryapi.DictionaryApi(
        os.environ['DICTIONARY_API_KEY'], root_dir / "words.sqlite3")

    entries = api_client.lookup(word)
    csv_writer = csv.writer(sys.stdout, delimiter=',', quotechar='"')

    first_url = None
    for entry in entries:
        stem = entry['meta']['id'].split(':', 1)[0]

        if stem == word:
            for pr in entry['hwi'].get('prs', []):
                if 'sound' not in pr:
                    continue

                url = pr_url(pr['sound']['audio'])
                if first_url is None:
                    first_url = url
                csv_writer.writerow(
                    [entry['meta']['id'], entry['fl'], pr['mw'], url])

        for uro in entry.get('uros', []):
            ure = uro['ure'].replace('*', '')
            if ure == word:
                for pr in uro['prs']:
                    if 'sound' not in pr:
                        continue

                    url = pr_url(pr['sound']['audio'])
                    if first_url is None:
                        first_url = url
                    csv_writer.writerow(
                        [ure, uro['fl'], pr['mw'], url])

    if download and first_url is not None:
        download_file(first_url)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    download = len(sys.argv) > 1 and sys.argv[1] == "-d"
    words = sys.argv[1:]
    if download:
        words = sys.argv[2:]

    for word in words:
        lookup_audio(Path(os.getcwd()), word, download)