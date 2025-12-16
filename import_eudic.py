#!/usr/bin/env python
import sys
import fileinput
import os
import re
from bs4 import BeautifulSoup, Comment, NavigableString
from pathlib import Path


def ensure_words_path(root_path: Path):
    root_path.mkdir(exist_ok=True, parents=True)
    return root_path / "words.txt"


def import_eudic(soup, root_path: Path):
    words_path = ensure_words_path(root_path)

    with open(words_path, "a", encoding="utf-8") as of:
        for row in soup.select(".export-table > tbody > tr"):
            cells = row.find_all("td", recursive=False)
            word = cells[1].get_text()
            definition = cells[4].find("div", class_="expDiv")

            # remove empty div
            for div in definition.find_all("div"):
                if len(div.contents) == 0:
                    div.decompose()
            # remove comments
            for node in definition.children:
                if isinstance(node, Comment):
                    node.extract()

            # Extract only the first example (before any <br>)
            # Preserve <b> tags in the example
            example_parts = []
            while definition.contents:
                node = definition.contents[0]
                if isinstance(node, NavigableString):
                    example_parts.append(str(node.extract()))
                elif getattr(node, "name", None) == "b":
                    # Keep <b> tags by converting to string (preserves HTML)
                    example_parts.append(str(node.extract()))
                elif getattr(node, "name", None) == "br":
                    # Stop at first <br> tag, don't extract it
                    break
                else:
                    break

            example = "".join(example_parts)
            # Cleanup: remove nbsp and squash consecutive spaces
            example = example.replace("&nbsp;", " ")  # HTML entity
            example = example.replace("\u00A0", " ")  # Unicode non-breaking space
            example = re.sub(r" +", " ", example).strip()  # Collapse consecutive spaces

            # Format: word: example (same as add_kindle_to_words.py)
            if example != '':
                of.write(f"{word}: {example}\n")

    return words_path


if __name__ == "__main__":
    input_files = (
        sys.argv[1:] if len(sys.argv) > 1 else os.environ.get("usage_file", "").split()
    )
    if not input_files or input_files == [""]:
        print(
            "No input files provided via arguments or usage_file environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)

    with fileinput.input(files=input_files, encoding="utf-8") as f:
        soup = BeautifulSoup("".join(f), "lxml")
    import_eudic(soup, Path(os.getcwd()))
