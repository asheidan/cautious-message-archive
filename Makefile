TARGET     = ./dist/MessageArchive.app
LOGDIR     = .logs
CACHEDIR   = .cache

VIRTUALENV = .virtualenv/PythonArchive
PIPCACHE   = $(CACHEDIR)/pip
PYTHON     = $(VIRTUALENV)/bin/python
PIP        = $(VIRTUALENV)/bin/pip
FLAKE      = $(VIRTUALENV)/bin/flake8
PYLINT     = $(VIRTUALENV)/bin/pylint

NODEENV    = frontend/node_modules
NODEBIN    = node_modules/.bin
GULP       = $(NODEBIN)/gulp
WEBPACK    = $(NODEBIN)/webpack
LESSC      = $(NODEBIN)/lessc

###############################################################################

PYS         = $(shell find backend -name '*.py' -type f)

JSXS        = $(shell find frontend/jsx -name '*.jsx' -type f)
JSBUNDLE    = frontend/dist/js/bundle.js

HTMLS       = frontend/html/index.html
HTMLBUNDLE  = frontend/dist/html/index.html

STYLES      = $(shell find frontend/less -name '*.less' -type f)
STYLEBUNDLE = frontend/dist/css/bundle.css

###############################################################################

$(TARGET): setup.py main.py $(STYLEBUNDLE) $(JSBUNDLE) $(HTMLBUNDLE) $(PYS) $(VIRTUALENV)
	sed -i "52s/^    m = mf.load_module(.*/    if hasattr(mf, 'load_module'):\n        m = mf.load_module(m.identifier, fp, pathname, stuff)\n    else:\n        m = mf._load_module(m.identifier, fp, pathname, stuff)/" $(VIRTUALENV)/lib/python3.5/site-packages/py2app/recipes/virtualenv.py
	$(PYTHON) $< py2app

dev: $(STYLEBUNDLE) $(JSBUNDLE) $(HTMLBUNDLE)
	$(PYTHON) -m backend --logging=debug
.PHONY: dev

server: $(VIRTUALENV)
	$(PYTHON) -m backend

launch: $(TARGET)
	open $(TARGET)
.PHONY: launch

###############################################################################

$(VIRTUALENV): requirements/application.pip | $(LOGDIR)
	test -d $@/bin || (mkdir -p $@ && virtualenv -p python3.5 $@)
	$(PIP) --log-file $(LOGDIR)/pip_error.log install --download-cache $(PIPCACHE) -r $< \
		&& touch -c $@ || touch -c -t 197001011200 $@

$(FLAKE) $(PYLINT): requirements/development.pip | $(VIRTUALENV) $(LOGDIR) $(PIPCACHE)
	$(PIP) --log-file $(LOGDIR)/pip_error.log install --download-cache $(PIPCACHE) -r $< \
		&& touch -c $(VIRTUALENV) $@ || touch -c -t 197001011200 $@

$(NODEENV): frontend/package.json
	cd frontend; npm install

###############################################################################

$(JSBUNDLE): frontend/webpack.config.js $(JSXS) $(NODEENV)
	@# --optimize-dedupe --optimize-occurence-order
	cd frontend; $(WEBPACK) --config $(<F)

$(STYLEBUNDLE): $(STYLES) $(NODEENV)
	cd frontend; $(LESSC) less/style.less dist/css/bundle.css

frontend/dist/html/%: frontend/html/%
	mkdir -p $(@D)
	cp $< $@

###############################################################################

$(LOGDIR) $(PIPCACHE):
	mkdir -p $@

###############################################################################

clean:
	$(RM) -r build dist frontend/dist
.PHONY: clean

distclean:
	$(RM) -r $(LOGDIR) $(VIRTUALENV) $(CACHEDIR)
.PHONY: distclean
