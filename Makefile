words:
	python gen_dict.py words.txt
	open -a Anki.app out/Words.csv

kindle:
	python gen_kindle_vocabulary.py
	cat out/kindle_vocabulary.txt >> words.txt

clean:
	rm -rf out

.PHONY: words clean
.PHONY: kindle
