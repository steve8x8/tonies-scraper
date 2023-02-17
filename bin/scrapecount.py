#!/usr/bin/python3

# Tonie track (and  more) scraper
# derived from Mahelita's work (Apr 2021)
# separate scrapers,   steve8x8: 09-12 Jan 2023
# all-in-one version,  steve8x8: 13 Jan 2023...

# only count tonies    steve8x8: 23 Jan 2023

from bs4 import BeautifulSoup
#from fuzzywuzzy import fuzz
import json
import numpy as np
import re
import requests
# also install python-Levenshtein
import sys
import datetime as dt



# stderr redirect
warnings = sys.stderr
#warnings = open('{base}.warn'.format(base = output_base), "w")


langs = [
  'de-de',
  'fr-fr',
  'en-gb',
  'en-eu',
  'en-us',
  'en-hk',
]


for lang in langs :
#  print("Working on language \"" + lang + "\"")

  if lang in [ 'de-de', 'en-gb', 'en-eu', 'fr-fr' ] :
# European server tonies.com
    url_base = 'https://tonies.com'
    if   lang == 'de-de' :
      ctonies = 'kreativ-tonies'
    elif lang == 'en-gb' :
      ctonies = 'creative-tonies'
    elif lang == 'en-eu' :
      ctonies = 'creative-tonies'
    elif lang == 'fr-fr' :
      ctonies = 'tonies-creatifs'
    else :
      ctonies = ''

    for what in [ 'tonies', ctonies ] :
      if ctonies == '' :
        continue
#      print(" Working on \"" + what + "\"")
      main_url = '{base}/{lang}/{what}/'.format(base = url_base, lang = lang, what = what)
      count = 0
      r = requests.get(main_url)
      if r.status_code == 200 :
        text = str(r.content)
        text = re.sub('\\\\x..', '(*)', text)
        for match in re.findall('Ho.rr*a[^0-9>]* [0-9][0-9]*[^>]*', text) :
          count = int(re.sub('[^0-9]*', '', match))
          break

      if count != 0 :
        print(f"{count:4}" + " " + what + " (" + lang + ")")

    # for what

  elif lang == 'en-hk' or \
       lang == 'en-us' :
    if lang == 'en-hk' :
      url_base = 'https://www.jselect.com'
      oembed = {
                'tonies' : '/en/collections/tonies.oembed',
                #'creative-tonies' : '/en/collections/creative-tonies.oembed'
               }
    elif lang =='en-us' :
      url_base = 'https://us.tonies.com'
      oembed = {
                'tonies' : '/collections/content.oembed'
               }
      # FIXME: no idea yet how to access creatie tonies
    #for what in [ 'tonies', ctonies ] :
    for what in oembed.keys() :
#      print(" Working on \"" + what + "\"")
      main_url = '{base}{path}'.format(base = url_base, path = oembed[what])
      count = 0
      r = requests.get(main_url)
      if r.status_code == 200 :
        text = str(r.content)
        text = re.sub('\\\\x..', '(*)', text)
        for match in re.findall('Ho.rr*a[^0-9>]* [0-9][0-9]*[^>]*', text) :
          count = (re.sub('[^0-9]*', '',  match))
          break


      if count != 0 :
        print(f"{count:4}" + " " + what + " (" + lang + ")")
    # for what
  # if lang
# for lang


if warnings != sys.stderr :
  warnings.close()
