#!/usr/bin/env make

SHELL=/bin/bash

PY=$(shell which python)


PYVER=python$(shell python -c "import sys ;print (sys.version[0:3])")

USER_SITE=$(HOME)/.local/lib/$(PYVER)/site-packages


ID=$(shell which id)

UID=$(shell id -u) 

HOME=$(shell printenv HOME)

ROOT=$(shell test $(UID) = 0 && echo 1 )



.PHONY:  all test install

all:
	@echo "To install type \"sudo make install\"" 

install:
	runner=`whoami` ; \
	if test $$runner != "root" ; \
	then \
		echo "You are not root. install to user local dir?"; \
		read -n 1 -r REPLY ; \
		if [[ $$REPLY =~ ^([yY]) ]] ; \
		then \
			$(PY) setup.py -v install --user --record "$(USER_SITE)/capitalize_installed_files.txt" ; \
		fi ;\
	else  \
	      sudo "$(PY)  setup.py -v install --record capitalize_installed_files.txt" ; \
        fi 

uninstall:
	@runner=`whoami` ; \
	if test $$runner != "root" ; \
	then \
	      echo "You are not root. Have password ready"; \
	      sudo "cat capitalize_installed_files.txt | xargs rm -rf"; \
        else \
                echo "You are root" ; \
	        cat capitalize_installed_files.txt | xargs rm -rf; \
        fi

test:
	@sh capitalize_test.sh


#
