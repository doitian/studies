#!/usr/bin/env python
import sys
import os
import re
import csv
import dictionaryapi
from pathlib import Path

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))

ALPHABET = re.compile(r"[a-zA-Z]")


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


def lookup_audio(root_dir: Path, word):
    api_client = dictionaryapi.DictionaryApi(
        os.environ['API_KEY'], root_dir / "words.sqlite3")

    entries = api_client.lookup(word)
    csv_writer = csv.writer(sys.stdout, delimiter=',', quotechar='"')
    for entry in entries:
        for pr in entry['hwi'].get('prs', []):
            csv_writer.writerow(
                [entry['hwi']['hw'], pr['mw'], pr_url(pr['sound']['audio'])])


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    lookup_audio(Path(os.getcwd()), sys.argv[1])
