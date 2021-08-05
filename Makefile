test:
	coverage run -m pytest
	coverage report -m *.py src/*.py

install:
	pip-upgrade *.txt
	pip install --force-reinstall -U -r requirements.txt
	pip install -r requirements.dev.txt
