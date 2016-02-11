SHELL=/bin/bash
VENV_NAME=venv

ifneq ($(wildcard ./$(VENV_NAME)/Scripts/activate),)
VENV_ACTIVATE=./$(VENV_NAME)/Scripts/activate
else
VENV_ACTIVATE=./$(VENV_NAME)/bin/activate
endif

# if `python` command is Python 3, use that, otherwise attempt to use `python3`
ifeq ($(shell python --version | sed -e 's/Python\s\([0-9]\).*/\1/'),3)
PYTHON = python
else
PYTHON = python3
endif


.PHONY: test upgrade freeze configure clean run debug build

freeze:
	source $(VENV_ACTIVATE); pip freeze > requirements.txt; deactivate

configure:
	npm install
	virtualenv -v -p 3 $(VENV_NAME)
	source $(VENV_ACTIVATE); pip install -r requirements.txt; deactivate

upgrade:
	npm upgrade --save-dev
	source $(VENV_ACTIVATE); pip install --upgrade -r requirements.txt; pip freeze > requirements.txt; deactivate

clean:
	rm -Rf node_modules/
	rm -Rf __pycache__/
	rm -Rf $(VENV_NAME)/
	rm -f *.css

test:
	source $(VENV_ACTIVATE); $(PYTHON) tests.py; deactivate
	$$(npm bin)/stylint $(CSS_DIR)/

run: build
	source $(VENV_ACTIVATE); $(PYTHON) whiteboard.py; deactivate

debug: build
	source $(VENV_ACTIVATE); $(PYTHON) whiteboard.py --debug; deactivate

build: whiteboard.css
	@echo 'build done'

%.css: %.styl
	$$(npm bin)/stylus -c -o $@ $*.styl
