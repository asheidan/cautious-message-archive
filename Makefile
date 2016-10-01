TARGET     = ./dist/MessageArchive.app
LOGDIR     = .logs
CACHEDIR   = .cache

VIRTUALENV = .virtualenv/PythonArchive
PIPCACHE   = $(CACHEDIR)/pip
PYTHON     = $(VIRTUALENV)/bin/python
PIP        = $(VIRTUALENV)/bin/pip
FLAKE      = $(VIRTUALENV)/bin/flake8
PYLINT     = $(VIRTUALENV)/bin/pylint

###############################################################################

$(TARGET): setup.py main.py $(VIRTUALENV)
	sed -i "52s/^    m = mf.load_module(.*/    if hasattr(mf, 'load_module'):\n        m = mf.load_module(m.identifier, fp, pathname, stuff)\n    else:\n        m = mf._load_module(m.identifier, fp, pathname, stuff)/" $(VIRTUALENV)/lib/python3.5/site-packages/py2app/recipes/virtualenv.py

	$(PYTHON) $< py2app

###############################################################################

$(VIRTUALENV): requirements/application.pip | $(LOGDIR)
	test -d $@/bin || (mkdir -p $@ && virtualenv -p python3.5 $@)
	$(PIP) --log-file $(LOGDIR)/pip_error.log install --download-cache $(PIPCACHE) -r $< \
		&& touch -c $@ || touch -c -t 197001011200 $@

$(FLAKE) $(PYLINT): requirements/development.pip | $(VIRTUALENV)
	$(PIP) --log-file $(LOGDIR)/pip_error.log install --download-cache $(PIPCACHE) -r $< \
		&& touch -c $(VIRTUALENV) $@ || touch -c -t 197001011200 $@

$(NODEENV): frontend/package.json
	cd frontend; npm install

###############################################################################

$(LOGDIR) $(PIPCACHE):
	mkdir -p $@

###############################################################################

clean:
	$(RM) -rf build dist
.PHONY: clean

distclean:
	$(RM) -rf $(LOGDIR) $(VIRTUALENV) $(CACHEDIR)
.PHONY: distclean
