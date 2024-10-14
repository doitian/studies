words: words.txt
	python gen_dict.py words.txt

kindle:
	python gen_kindle_vocabulary.py

eudic:
	python gen_eudic_vocabulary.py eudic.html

eudic-archive:
	python add_to_eudic.py --book Archive --move words.txt

kindle-archive:
	python add_to_eudic.py --book Kindle words.txt

clean:
	rm -rf out eudic.html

.PHONY: words clean kindle eudic eudic-archive kindle-archive