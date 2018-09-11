words:
	pipenv run python gen_dict.py '/Users/ian/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/words.txt'
	open out/Words.studyarch

clean:
	rm -rf out

.PHONE: words clean
