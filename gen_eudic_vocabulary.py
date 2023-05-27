#!/usr/bin/env python
import fileinput
import os
import re
from bs4 import BeautifulSoup
from pathlib import Path

WORDS_FILE_NAME = 'eudict_vocabulary.txt'


def ensure_words_path(root_path: Path):
    out_dir = root_path / 'out'
    out_dir.mkdir(exist_ok=True, parents=True)
    return out_dir / WORDS_FILE_NAME


def gen_eudic_vocabulary(soup, root_path: Path):
    words_path = ensure_words_path(root_path)

    with open(words_path, "w") as of:
        for row in soup.select('.export-table > tbody > tr'):
            cells = row.find_all('td', recursive=False)
            word = cells[1].get_text()
            definition = cells[4].find('div', class_='expDiv')
            del definition['id']
            definition['class'] = 'cobuild'

            # remove stylesheets
            for css in definition.select('link[rel="stylesheet"]'):
                css.decompose()
            # remove empty div
            for div in definition.find_all('div'):
                if len(div.contents) == 0:
                    div.decompose()

            for a in definition.find_all('a', href=True):
                if a['href'].startswith('https://cn.eudic.net/dict/searchword?'):
                    a['href'] = f"eudic://dict/{a['href'].split('?word=')[1]}"

            definition_text = ' '.join(str(definition).splitlines())

            print("{0} :{1}".format(word, definition_text), file=of)

    return words_path


if __name__ == '__main__':
    with fileinput.input(encoding="utf-8") as f:
        soup = BeautifulSoup(''.join(f), 'html.parser')
    gen_eudic_vocabulary(soup, Path(os.getcwd()))