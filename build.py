#!/usr/bin/env python
import os
import csv
import fileinput
from pathlib import Path


def build(root_dir: Path, input):
    out_dir = root_dir / 'out'
    out_dir.mkdir(parents=True, exist_ok=True)

    data_csv = out_dir / 'Words.csv'

    with open(data_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"')

        csv_writer.writerow(['#separator:Comma'])
        csv_writer.writerow(['#html:true'])
        csv_writer.writerow(['#deck:English Learning::Word in Sentence'])
        csv_writer.writerow(['#notetype:_word-in-sentence'])

        for line in input:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Parse format: word: example
            parts = [p.strip() for p in line.split(':', maxsplit=1)]
            if len(parts) != 2:
                continue

            word, example = parts
            if word == '':
                continue

            # Create eudic link
            encoded_word = word.replace(" ", "%20")
            eudic_link = f'eudic://dict/{encoded_word}'

            # Write row: word, example, eudic_link
            csv_writer.writerow([word, example, eudic_link])


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    build(Path(os.getcwd()), fileinput.input())