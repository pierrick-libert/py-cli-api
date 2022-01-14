# Makefile

all: install

clean:
	rm -rf env/

install:
	python3.9 -m venv env
	. env/bin/activate && python  -m pip install --upgrade pip
	. env/bin/activate && pip install -r requirements.txt
	. env/bin/activate && python init_db.py

lint:
	. env/bin/activate && pylint --fail-under 9.0 --disable=duplicate-code *.py utils/*.py models/*.py modules/*.py

test:
	. env/bin/activate && python test.py 

greenkeeping:
	. env/bin/activate && pur -r requirements.txt
