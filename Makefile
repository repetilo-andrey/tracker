# -*- makefile -*-

# definitions
PROJECT       = tracker
HOST          = 127.0.0.1
PORT          = 9999
CURRPATH      = $(shell pwd)
PIDFILE       = $(shell pwd)/etc/django.pid


PROJECT_TEST_TARGETS=timing

# constants
PYTHONPATH = .:..
PYTHON     = python

MANAGE=cd $(PROJECT) && PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings django-admin.py

# end

run:
	$(MAKE) clean
	$(MANAGE) runserver $(HOST):$(PORT)

syncdb:
	$(MAKE) clean
	$(MANAGE) syncdb --noinput
	$(MAKE) manage -e CMD="migrate"

fresh_syncdb:
	-rm dev.db
	$(MANAGE) syncdb
	$(MAKE) manage -e CMD="migrate"
	@echo Loading initial fixtures...
	$(MANAGE) loaddata base_initial_data.json
	$(MANAGE) loaddata cron.json
	@echo Done

test:
	$(MAKE) clean
	TESTING=1 $(MANAGE) test --verbosity=2 $(TEST_OPTIONS) $(PROJECT_TEST_TARGETS)

jenkins:
	$(MAKE) clean
	TESTING=1 $(MANAGE) jenkins $(TEST_OPTIONS) $(PROJECT_TEST_TARGETS)

clean:
	@echo Cleaning up *.pyc files
	-find . | grep '.pyc$$' | xargs -I {} rm {}

convert:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting of migration of $(APP_NAME)
	$(MANAGE) convert_to_south $(APP_NAME)
	@echo Done
endif

migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting of migration of $(APP_NAME)
	-$(MANAGE) schemamigration $(APP_NAME) --auto
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

init_migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting init migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --initial
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

manage:
ifndef CMD
	@echo Please, specify CMD argument to execute Django management command
else
	$(MANAGE)  $(CMD)
endif

help:
	@cat README

mail:
	python -m smtpd -n -c DebuggingServer localhost:1025

shell:
	$(MAKE) clean
	$(MANAGE) shell_plus
