#!/usr/bin/env python
import os
import io
import csv
import fileinput
import dictionaryapi
import lxml.html
from io import BytesIO, StringIO
from lxml import etree
from pathlib import Path
from shutil import rmtree, make_archive, move

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))


def gen_dict(root_dir: Path, input):
    xslt_doc = etree.parse(str(script_dir / "dictionaryapi.xslt"))
    xslt_transformer = etree.XSLT(xslt_doc)

    out_dir = root_dir / 'out' / 'Words'
    dir_archive = out_dir / 'Archive'
    dir_words = dir_archive / 'Groups' / 'Words'
    dir_words.mkdir(parents=True, exist_ok=True)
    (dir_archive / 'Ungrouped').mkdir(exist_ok=True)

    data_csv = dir_words / 'Data.csv'
    api_client = dictionaryapi.DictionaryApi(os.environ['API_KEY'], root_dir / "words.sqlite3")

    with open(data_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        csv_writer.writerow(['1 Text', '2 HTML', '3 Text'])
        for line in input:
            parts = [p.strip() for p in line.split(':', maxsplit=1)]
            word, example = parts if len(parts) == 2 else (parts[0], '')
            if word != '':
                print("lookup {0}".format(word))
                r = api_client.lookup(word)
                doc = etree.parse(BytesIO(r.encode('utf-8')))
                word_stem = doc.xpath("//ew")[0].text
                if word != word_stem:
                    word = word_stem + ' > ' + word
                buffer = BytesIO()
                xslt_transformer(doc).write(buffer)
                csv_writer.writerow([word, buffer.getvalue().decode('utf-8'), example])

    # with open(data_csv, 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    #     csv_writer.writerow(['1 Text', '2 HTML'])
    #     doc = etree.parse('friend.xml')
    #     buffer = BytesIO()
    #     xslt_transformer(doc).write(buffer, pretty_print=True)
    #     print(buffer.getvalue().decode('utf-8'))
    #     csv_writer.writerow(['friend', buffer.getvalue().decode('utf-8')])

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
