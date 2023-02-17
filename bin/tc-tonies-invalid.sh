#!/bin/bash

# find invalid urls from tc-tonies.json
egrep '"(title|url)' ${1:-tc-tonies.json} \
| grep -B2 url_invalid \
| grep -v '^--' \
| sed 's~.*url_invalid.*~~' \
> tc-tonies-invalid.list

