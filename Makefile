#!/usr/bin/make -f

export BIN:=$(shell pwd -P)/bin

# base function
default:	orig club tonies

# be able to diff against previous run
all:		save orig club tonies diff

save:
	@for file in \
	    *.json \
	    *.list \
	    *.warn ; \
	do \
	    cp -pi $${file} $${file}.SAVE ; \
	done
	@true

# fetch original (Gambrius) tonies.json as orig-tonies.json
orig:
	@echo "Get official tonies.json ..."
	@$(BIN)/orig-tonies.get
	@echo "... done."

# fetch data from tonies.club (to be merged later)
club:
	@echo "Scrape tonies.club ..."
	@$(BIN)/tc-scraper.py
	@$(BIN)/deraw tc-tonies.raw.json
	@$(BIN)/tc-tonies-invalid.sh
	@echo "... done.'

# fetch data from tonies.com
tonies:
	@echo "Scrape tonies.com ..."
	@$(BIN)/scraper.py
	@$(BIN)/deraw tonies.raw.json
	@echo "... done."

# show differences
diff:
	@for file in \
	    tc-tonies-invalid.list \
	    tonies.warn \
	    tonies.json ; \
	do \
	    echo diff for $${file}: ; \
	    diff -u $${file}.SAVE $${file} ; \
	    read -p "continue ... -> " x ; \
	done

PHONY:	default all save orig club tonies diff
