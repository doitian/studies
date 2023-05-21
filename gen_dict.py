#!/usr/bin/env python
import os
import csv
import html
import fileinput
import dictionaryapi
import re
from pathlib import Path
from jinja2 import Template

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))


def gen_dict(root_dir: Path, input):
    template = Template(open(script_dir / "dictionaryapi.html.jinja").read())

    out_dir = root_dir / 'out'
    out_dir.mkdir(parents=True, exist_ok=True)

    data_csv = out_dir / 'Words.csv'
    api_client = dictionaryapi.DictionaryApi(
        os.environ['API_KEY'], root_dir / "words.sqlite3")

    with open(data_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"')

        csv_writer.writerow(['#separator:Comma'])
        csv_writer.writerow(['#html:true'])
        csv_writer.writerow(['#deck:English Learning::English Vocabulary'])
        csv_writer.writerow(['#notetype:ian-basic'])

        for line in input:
            parts = [p.strip() for p in line.split(':', maxsplit=1)]
            word, example = parts if len(parts) == 2 else (parts[0], '')
            if word != '':
                print("lookup {0}".format(word))
                entries = api_client.lookup(word)
                stem = entries[0]['meta']['id'].split(':', 1)[0]
                definition = template.render(
                    entries=entries, word=word, stem=stem)
                if word != stem:
                    word = stem + ' > ' + word
                if not example.startswith('<'):
                    example = html.escape(example)
                    example = re.sub(r'(?<!\\)\*\*(?<!\\)(.*?[^\\])\*\*', r'<b>\1</b>', example)
                    example = re.sub(r'(?<!\\)\*(.*?[^\\])\*', r'<i>\1</i>', example)
                csv_writer.writerow(
                    [html.escape(word), '{}<hr /><blockquote>{}</blockquote>'.format(definition, example)])


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    gen_dict(Path(os.getcwd()), fileinput.input())