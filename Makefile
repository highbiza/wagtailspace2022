.PHONY: fail-if-no-virtualenv all install loaddata test

all: install migrate loaddata collectstatic

fail-if-no-virtualenv:
ifndef VIRTUAL_ENV # check for a virtualenv in development environment
ifndef PYENVPIPELINE_VIRTUALENV # check for jenkins pipeline virtualenv
$(error this makefile needs a virtualenv)
endif
endif

ifndef PIP_INDEX_URL
PIP_INDEX_URL=https://pypi.uwkm.nl/oxyan/testing/+simple/
endif


install: fail-if-no-virtualenv
	npm install
	npm run build
	pip install -e git+https://github.com/highbiza/wagtail-roadrunner.git#egg=wagtail-roadrunner
	pip install -e .

roadrunner:
	echo "go into your virtualenv cdvirtualenv && cd src/roadrunner && npm install && npm run build"


migrate:
	manage.py migrate --no-input

loaddata:
	# manage.py loaddata

collectstatic:
	manage.py collectstatic --no-input

lint: fail-if-no-virtualenv
	@black --check --exclude "migrations/*" oxyan
	@pylint setup.py oxyan/

test: fail-if-no-virtualenv
	@coverage run --source='oxyan' `which manage.py` test
	@coverage report
	@coverage xml
	@coverage html
	npm audit

black:
	@black --exclude "migrations/*" oxyan sandbox
