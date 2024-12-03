# Makefile

all: install

clean:
	rm -rf env/

install:
	pip install -r requirements.txt
	pre-commit install
	pre-commit autoupdate
	python init_db.py

lint:
	sh check_pylint_score.sh

greenkeeping:
	pur -r requirements.txt
