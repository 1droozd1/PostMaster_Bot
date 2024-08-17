.PHONY: venv
.PHONY: run
.PHONY: test

venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
run:
	./venv/bin/python3 ./src/main.py

test:
	./venv/bin/python3 ./src/test.py