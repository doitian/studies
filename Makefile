words:
	pipenv run python gen_dict.py words.txt
	open out/Words.studyarch

kindle_extract:
	pipenv run python gen_kindle_vocabulary.py

kindle_gen:
	pipenv run python gen_dict.py out/kindle_vocabulary.txt
	open out/Words.studyarch

clean:
	rm -rf out

.PHONY: words clean
.PHONY: kindle_extract kindle_gen
