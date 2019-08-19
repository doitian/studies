import csv
import os
import sys
from pathlib import Path
from html import escape

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))

html_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{0}</title>
<style>
{1}
</style>
</head>

<body>
{2}
</body>

</html>
"""


def to_html(root):
    with open(script_dir / 'sakura.css') as css_file:
        css_content = css_file.read()

    with open(root / 'Data.csv', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        html_body = ''
        for row in reader:
            cols = []
            for (name, content) in row.items():
                if content is None:
                    content = ''

                col, content_type = name.split(' ', 1)
                col = int(col) - 1
                if content_type == 'HTML':
                    formatted_content = content
                elif content_type == 'Image':
                    formatted_content = '<figure><img src="{0}" /></figure>'.format(escape(content, quote=True))
                elif content != '':
                    formatted_content = '<p>{0}</p>'.format(escape(content))
                else:
                    formatted_content = ''

                if len(cols) <= col:
                    cols.append(formatted_content)

                if content != '':
                    if content_type == 'HTML':
                        cols[col] = content

                    if content_type == 'Image' and cols[col] != formatted_content:
                        cols[col] = cols[col] + '<br />' + formatted_content

            html_body += "  <hr /><h2>{0}</h2>\n".format(cols[0])
            for content in cols[1:]:
                if content != '':
                    html_body += content + "\n"

        html_file_path = root / (root.name + '.html')
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_template.format(escape(root.name), css_content, html_body))
            print('Created {0}'.format(html_file_path))


if __name__ == "__main__":
    for root, dirs, files in os.walk(sys.argv[1]):
        if 'Data.csv' in files:
            to_html(Path(root))
