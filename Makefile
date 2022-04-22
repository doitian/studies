SHORTCUTS_WORDS := "$$HOME/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/words.txt"

words:
	! [ -e ${SHORTCUTS_WORDS} ] || (( $$(cat ${SHORTCUTS_WORDS} | wc -l) == 0 ))
	python gen_dict.py words.txt
	open -a Anki.app out/Words.csv

kindle:
	python gen_kindle_vocabulary.py
	cat out/kindle_vocabulary.txt >> words.txt

clean:
	rm -rf out

.PHONY: words clean
.PHONY: kindle