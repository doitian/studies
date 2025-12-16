# Scripts for English Studies

This repository provides a set of scripts for building Anki flashcards to review English vocabulary.

## Setup

This project uses [mise](https://mise.jdx.dev/) for task management. Install dependencies and run tasks using mise:

    mise install
    mise run <task>

### Configuration

Configure environment variables in `mise.local.toml` (this file is gitignored). For example, to configure the Eudic API token:

```toml
[env]
EUDIC_TOKEN = "your-token-here"
```

## English Words

### Building CSV from words.txt

Create `out/Words.csv` from `words.txt`:

    mise run build

The `words.txt` file uses the format `word: example`, where each line contains a word and its example sentence separated by a colon. The example can include HTML tags like `<b>` for emphasis.

The CSV file can be imported into Anki.

### Importing Words

Import words from Kindle vocabulary database:

    mise run import:kindle

This extracts new words from the Kindle vocabulary database and appends them to `words.txt`.

Import words from Eudic exported vocabulary book:

    mise run import:eudic <file.html>

This extracts words from an Eudic HTML export file and appends them to `words.txt`.

## Eudic Vocabulary Management

Move the words in `words.txt` to the Archive book:

    mise run archive:eudic

Add the words in `words.txt` to the Kindle book:

    mise run archive:kindle

## Other Tasks

Empty `words.txt`:

    mise run empty

Clean output files:

    mise run clean
