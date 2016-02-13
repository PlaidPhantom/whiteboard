SHELL=/bin/bash
VENV_NAME=venv
CSS_DIR=css
JS_DIR=js

VENV_ACTIVATE = ./$(VENV_NAME)/*/activate

# if `python` command is Python 3, use that, otherwise attempt to use `python3`
ifeq ($(shell python --version | sed -e 's/Python\s\([0-9]\).*/\1/'),3)
PYTHON = python
else
PYTHON = python3
endif


.PHONY: freeze configure-dev configure upgrade clean test run debug build

all: build

freeze:
	source $(VENV_ACTIVATE) && pip freeze > requirements.txt && deactivate

configure-dev: configure
	npm install
	pip install -r requirements-dev.txt

configure:
	npm install --production
	virtualenv -v -p 3 $(VENV_NAME)
	source $(VENV_ACTIVATE) && pip install -r requirements.txt && deactivate

upgrade:
	npm upgrade --save-dev
	source $(VENV_ACTIVATE) && pip install --upgrade -r requirements.txt && pip freeze > requirements.txt && deactivate

clean:
	rm -Rf node_modules/
	rm -Rf __pycache__/
	rm -Rf $(VENV_NAME)/
	rm -f $(CSS_DIR)/*.css
	rm -f $(JS_DIR)/*.min.js
	rm -f $(JS_DIR)/*.js

test:
	source $(VENV_ACTIVATE) && $(PYTHON) tests.py && deactivate
	$$(npm bin)/stylint $(CSS_DIR)/

run: build
	source $(VENV_ACTIVATE) && $(PYTHON) whiteboard.py && deactivate

debug: build
	source $(VENV_ACTIVATE) && $(PYTHON) whiteboard.py --debug && deactivate

build: $(CSS_DIR)/whiteboard.css $(JS_DIR)/whiteboard.min.js
	@echo 'build done'

%.css: %.styl
	$$(npm bin)/stylus -c -o $@ $?

%.min.js: %.js
	$$(npm bin)/uglifyjs -o $@ $?

%.js: %.es
	$$(npm bin)/babel -o $@ $?