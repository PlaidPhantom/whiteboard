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


.PHONY: pip-install pip-uninstall configure-dev configure upgrade clean clean-env test run debug kill build build-debug

all: build

pip-install:
	# usage: make pip-install PKG=<package name>
	source $(VENV_ACTIVATE) && pip install $(PKG) && pip freeze > requirements.txt && deactivate

pip-uninstall:
	# usage: make pip-uninstall PKG=<package name>
	source $(VENV_ACTIVATE) && pip uninstall $(PKG) && pip freeze > requirements.txt && deactivate

configure-dev: configure
	npm install
	pip install -r requirements-dev.txt

configure:
	npm install --production
	virtualenv -v -p $(PYTHON) $(VENV_NAME)
	source $(VENV_ACTIVATE) && pip install -r requirements.txt && deactivate
	./install-redis.sh

upgrade:
	npm upgrade --save-dev
	source $(VENV_ACTIVATE) && pip install --upgrade -r requirements.txt && pip freeze > requirements.txt && deactivate

clean:
	rm -f $(CSS_DIR)/*.css
	rm -f $(JS_DIR)/*.min.js
	rm -f $(JS_DIR)/*.js
	rm -f $(JS_DIR)/*.bundle.js

clean-env:
	rm -Rf node_modules/
	rm -Rf __pycache__/
	rm -Rf $(VENV_NAME)/


test:
	source $(VENV_ACTIVATE) && $(PYTHON) tests.py && deactivate
	$$(npm bin)/stylint $(CSS_DIR)/

run: build
	./redis.sh & echo $$! > redis.pid
	./site.sh & echo $$! > site.pid
	./web-socket.sh & echo $$! > web-socket.pid
	./proxy.sh & echo $$! > proxy.pid

debug: build-debug
	./redis.sh --loglevel verbose & echo $$! > redis.pid
	./site.sh --debug & echo $$! > site.pid
	./web-socket.sh --debug & echo $$! > web-socket.pid
	./proxy.sh & echo $$! > proxy.pid

stop:
	kill $$(cat *.pid) && rm *.pid

build: $(CSS_DIR)/whiteboard.css $(JS_DIR)/whiteboard.min.js $(JS_DIR)/index.min.js
	@echo 'build done'

build-debug: $(CSS_DIR)/whiteboard.css $(JS_DIR)/whiteboard.bundle.js $(JS_DIR)/index.bundle.js
	@echo 'build done'

%.css: %.styl
	$$(npm bin)/stylus --resolve-url --include-css --compress --out $@ $?

%.min.js: %.bundle.js
	$$(npm bin)/uglifyjs -o $@ $?

$(JS_DIR)/whiteboard.bundle.js: $(JS_DIR)/libs/bliss.js $(JS_DIR)/SocketClient.js $(JS_DIR)/whiteboard.js
	./bundle.sh $@ $+

$(JS_DIR)/index.bundle.js: $(JS_DIR)/libs/knockout-3.4.0.js $(JS_DIR)/libs/bliss.js $(JS_DIR)/index.js
	./bundle.sh $@ $+

%.js: %.es
	$$(npm bin)/babel -o $@ $?
