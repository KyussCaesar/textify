test: test1

test1:
	./textify.py ./testing/test1.text
	diff ./testing/test1.html ./testing/test1-cmp.html
