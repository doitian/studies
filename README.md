# Scripts for Studies

The archive format specification of `StudyArch`, which is supported by
Studies, can be found [here](http://www.studiesapp.com/studyarch/).

This repository is a collection of scripts to create Studies stacks.

First copy the example `.env` file and edit it.

    cp env.example .env

Then install dependencies using `pipenv`

    pipenv install

## English Words

Create `out/Words.studyarch` from a words file.

    pipenv run python gen_dict.py words.txt

Where each line in the words file is a word to learn. An example can be added
by separated it with ` :` from the word. See the `words.txt` as an example.

There is also a script to extract words from Kindle vocabulary builder

    pipenv run python gen_kindle_vocabulary.py

The generated words file is in `out/kindle_vocabulary.txt`
