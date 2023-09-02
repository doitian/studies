words: words.txt
	python gen_dict.py words.txt
	open -a Anki.app out/Words.csv

words.txt:
	ln -snf "$$HOME/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/words.txt" words.txt

kindle:
	python gen_kindle_vocabulary.py

eudic:
	python gen_eudic_vocabulary.py

clean:
	rm -rf out

.PHONY: words clean kindle eudic