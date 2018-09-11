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
from dotenv import load_dotenv

load_dotenv()

xslt_doc = etree.parse("dictionaryapi.xslt")
xslt_transformer = etree.XSLT(xslt_doc)

out_dir = Path('out') / 'Words'
dir_archive = out_dir / 'Archive'
dir_words = dir_archive / 'Groups' / 'Words'
dir_words.mkdir(parents=True, exist_ok=True)
(dir_archive / 'Ungrouped').mkdir(exist_ok=True)

data_csv = dir_words / 'Data.csv'
api_client = dictionaryapi.DictionaryApi(os.environ['API_KEY'], "words.sqlite3")

with open(data_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    csv_writer.writerow(['1 Text', '2 HTML', '3 Text'])
    for line in fileinput.input():
        parts = line.strip().split(" >", maxsplit=1)
        word, example = parts if len(parts) == 2 else (parts[0], '')
        if word != '':
            print("lookup {0}".format(word))
            r = api_client.lookup(word)
            doc = etree.parse(BytesIO(r.encode('utf-8')))
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
target = Path('out') / 'Words.studyarch'
src = Path('out') / 'Words.zip'
if target.exists():
    target.unlink()
move(src, target)
