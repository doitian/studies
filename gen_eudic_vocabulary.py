#!/usr/bin/env python
import fileinput
import os
import datetime
from bs4 import BeautifulSoup, Comment, NavigableString
from pathlib import Path


def ensure_words_path(root_path: Path):
    root_path.mkdir(exist_ok=True, parents=True)
    return root_path / 'words.txt'


def gen_eudic_vocabulary(soup, root_path: Path):
    words_path = ensure_words_path(root_path)

    with open(words_path, "a") as of:
        print(f'\n# {datetime.datetime.now().isoformat()}', file=of)
        for row in soup.select('.export-table > tbody > tr'):
            cells = row.find_all('td', recursive=False)
            word = cells[1].get_text()
            definition = cells[4].find('div', class_='expDiv')

            # remove empty div
            for div in definition.find_all('div'):
                if len(div.contents) == 0:
                    div.decompose()
            # remove comments
            for node in definition.children:
                if isinstance(node, Comment):
                    node.extract()
            # convert links
            for a in definition.find_all('a', href=True):
                if a['href'].startswith('https://cn.eudic.net/dict/searchword?'):
                    a['href'] = f"eudic://dict/{a['href'].split('?word=')[1]}"
            for img in definition.find_all('img'):
                if img['src'].startswith('file:'):
                    img['src'] = '_'.join(img['src'].split('/')[-2:])[1:]
            for css in definition.select('link[rel="stylesheet"]'):
                style_tag = soup.new_tag('style')
                style_path = '_'.join(css['href'].split('/')[-2:])
                style_tag.string = f'@import url("{style_path}")'
                css.replace_with(style_tag)
            for script in definition.select('script'):
                script.decompose()

            example = ''
            if isinstance(definition.contents[0], NavigableString):
                example = '\\n'.join(
                    str(definition.contents[0].extract()).splitlines())

            definition_text = ''.join(str(definition).splitlines())

            print("{} :={}=:{}".format(word, definition_text, example), file=of)

    return words_path


if __name__ == '__main__':
    with fileinput.input(encoding="utf-8") as f:
        soup = BeautifulSoup(''.join(f), 'html.parser')
    gen_eudic_vocabulary(soup, Path(os.getcwd()))