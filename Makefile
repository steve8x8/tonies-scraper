#!/usr/bin/make -f

export BIN:=$(shell pwd -P)/bin
export DAT:=$(shell date "+%Y-%m-%d")

# base function
default:	orig club tonies

# be able to diff against previous run
all:		save orig club tonies diff

save:
	@echo ""
	@for file in \
	    *.json \
	    *.list \
	    *.warn ; \
	do \
	    cp -pi $${file} $${file}.SAVE || true ; \
	done

store:
	@echo ""
	@mkdir -p SAVED/$(DAT)
	@for file in \
	    *.json \
	    *.list \
	    *.warn ; \
	do \
	    cp -pi $${file} SAVED/$(DAT) || true ; \
	done
	@rm -f SAVED/$(DAT)/*.raw.json || true

clean:
	@rm -f *.SAVE

# fetch original (Gambrius) tonies.json as orig-tonies.json
orig:
	@echo ""
	@echo "Get official tonies.json ..."
	@$(BIN)/orig-tonies.get
	@echo "... done."

# fetch data from tonies.club (to be merged later)
club:
	@echo ""
	@echo "Scrape tonies.club ..."
	@$(BIN)/tc-scraper.py
	@$(BIN)/deraw tc-tonies.raw.json && rm tc-tonies.raw.json
	@$(BIN)/tc-tonies-invalid.sh
	@echo "... done."

# fetch data from tonies.com
tonies:
	@echo ""
	@echo "Scrape tonies.com ..."
	@$(BIN)/scraper.py
	@$(BIN)/deraw tonies.raw.json && rm tonies.raw.json
	@echo "... done."

# show differences
diff:
	@echo ""
	@for file in \
	    tc-tonies-invalid.list \
	    tonies.warn \
	    tonies.json ; \
	do \
	    echo "" ; \
	    read -p "diff for $${file}: -> " x ; \
	    diff -u $${file}.SAVE $${file} ; \
	    read -p "continue -> " x ; \
	done

PHONY:	default all save orig club tonies diff
