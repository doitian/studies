#!/usr/bin/env python
import os
import io
import csv
import fileinput
import dictionaryapi
from pathlib import Path
from shutil import make_archive, move
from jinja2 import Template

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))


def gen_dict(root_dir: Path, input):
    template = Template(open(script_dir / "dictionaryapi.html.jinja").read())

    out_dir = root_dir / 'out' / 'Words'
    dir_archive = out_dir / 'Archive'
    dir_words = dir_archive / 'Groups' / 'Words'
    dir_words.mkdir(parents=True, exist_ok=True)
    (dir_archive / 'Ungrouped').mkdir(exist_ok=True)

    data_csv = dir_words / 'Data.csv'
    api_client = dictionaryapi.DictionaryApi(
        os.environ['API_KEY'], root_dir / "words.sqlite3")

    with open(data_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        csv_writer.writerow(['1 Text', '2 HTML', '3 Text'])
        for line in input:
            parts = [p.strip() for p in line.split(':', maxsplit=1)]
            word, example = parts if len(parts) == 2 else (parts[0], '')
            if word != '':
                print("lookup {0}".format(word))
                entries = api_client.lookup(word)
                word_stem = entries[0]['hwi']['hw']
                if word != word_stem:
                    word = word_stem + ' > ' + word
                html = template.render(entries=entries)
                csv_writer.writerow(
                    [word, html, example])

    # with open(data_csv, 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    #     csv_writer.writerow(['1 Text', '2 HTML'])
    #     import json
    #     entries = json.load(open('friend.json'))
    #     html = template.render(entries=entries)
    #     print(html)
    #     csv_writer.writerow(['friend', html])

    make_archive(out_dir, 'zip', out_dir)
    target = root_dir / 'out' / 'Words.studyarch'
    src = root_dir / 'out' / 'Words.zip'
    if target.exists():
        target.unlink()
    move(src, target)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    gen_dict(Path(os.getcwd()), fileinput.input())
