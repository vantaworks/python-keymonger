# Test options
TESTSCRIPT    ?= tests.py

# TODO: PEX
# TODO: REPO
# TODO: Maybe static typing with mypy

help:
	@echo "Available Options:"
	@echo "    lint: lint evertyhing in the coinmetrics directory."

clean:
	rm -f authorized_keys

lint:
	pylint keymonger/*.py

lint-extras:
	pylint test.py

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -rf .mypy_cache/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	rm -f authorized_keys
	rm -f *.pub

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

requirements.txt:
	pip -q install pipreqs
	pipreqs --no-pin

test:
	python3 $(TESTSCRIPT) || python $(TESTSCRIPT)

clean: clean-build clean-pyc

coverage:
	coverage run $(TESTSCRIPT)
	coverage report --include="keymonger/*" -m

coverage-upload: coverage
	pip install -q codecov
	codecov

release: requirements.txt clean 
	python setup.py sdist
	python setup.py bdist_wheel
	pip install twine
	twine upload dist/*

install: clean
	python setup.py develop

