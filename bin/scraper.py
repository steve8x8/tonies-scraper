#!/usr/bin/python3

# Tonie track (and  more) scraper
# derived from work by Mahelita:  Apr 2021
# separate scrapers,   steve8x8: 09-12 Jan 2023
# all-in-one version,  steve8x8: 14 Jan 2023
# merge tonies.club    steve8x8: 23 Jan 2023
# updates for new unknown strings...


from bs4 import BeautifulSoup
#from fuzzywuzzy import fuzz
import json
import numpy as np
import re
import requests
# also install python-Levenshtein
import sys
import datetime as dt



#output_base = 'new_tonies'
output_base = 'tonies'

# stderr redirect
#warnings = sys.stderr
warnings = open('{base}.warn'.format(base = output_base), "w")



# clean embedded JSON - don't blame me for this code
def cleanJson(text) :
  newtext = str(text)
  # umlauts etc
  newtext = re.sub('\\\\xc2\\\\xa0', ' ', newtext) # hard space
  newtext = re.sub('\\\\xc2\\\\xa1', '¡', newtext)
  newtext = re.sub('\\\\xc2\\\\xa2', '¢', newtext)
  newtext = re.sub('\\\\xc2\\\\xa3', '£', newtext)
  newtext = re.sub('\\\\xc2\\\\xa4', '¤', newtext)
  newtext = re.sub('\\\\xc2\\\\xa5', '¥', newtext)
  newtext = re.sub('\\\\xc2\\\\xa6', '¦', newtext)
  newtext = re.sub('\\\\xc2\\\\xa7', '§', newtext)
  newtext = re.sub('\\\\xc2\\\\xa8', '¨', newtext)
  newtext = re.sub('\\\\xc2\\\\xa9', '©', newtext)
  newtext = re.sub('\\\\xc2\\\\xaa', 'ª', newtext)
  newtext = re.sub('\\\\xc2\\\\xab', '«', newtext)
  newtext = re.sub('\\\\xc2\\\\xac', '¬', newtext)
  newtext = re.sub('\\\\xc2\\\\xad', ' ', newtext)
  newtext = re.sub('\\\\xc2\\\\xae', '®', newtext)
  newtext = re.sub('\\\\xc2\\\\xaf', '¯', newtext)
  newtext = re.sub('\\\\xc2\\\\xb0', '°', newtext)
  newtext = re.sub('\\\\xc2\\\\xb1', '±', newtext)
  newtext = re.sub('\\\\xc2\\\\xb2', '²', newtext)
  newtext = re.sub('\\\\xc2\\\\xb3', '³', newtext)
  newtext = re.sub('\\\\xc2\\\\xb4', '´', newtext)
  newtext = re.sub('\\\\xc2\\\\xb5', 'µ', newtext)
  newtext = re.sub('\\\\xc2\\\\xb6', '¶', newtext)
  newtext = re.sub('\\\\xc2\\\\xb7', '·', newtext)
  newtext = re.sub('\\\\xc2\\\\xb8', '¸', newtext)
  newtext = re.sub('\\\\xc2\\\\xb9', '¹', newtext)
  newtext = re.sub('\\\\xc2\\\\xba', 'º', newtext)
  newtext = re.sub('\\\\xc2\\\\xbb', '»', newtext)
  newtext = re.sub('\\\\xc2\\\\xbc', '¼', newtext)
  newtext = re.sub('\\\\xc2\\\\xbd', '½', newtext)
  newtext = re.sub('\\\\xc2\\\\xbe', '¾', newtext)
  newtext = re.sub('\\\\xc2\\\\xbf', '¿', newtext)
  #
  newtext = re.sub('\\\\xc3\\\\x80', 'À', newtext)
  newtext = re.sub('\\\\xc3\\\\x81', 'Á', newtext)
  newtext = re.sub('\\\\xc3\\\\x82', 'Â', newtext)
  newtext = re.sub('\\\\xc3\\\\x83', 'Ã', newtext)
  newtext = re.sub('\\\\xc3\\\\x84', 'Ä', newtext)
  newtext = re.sub('\\\\xc3\\\\x85', 'Å', newtext)
  newtext = re.sub('\\\\xc3\\\\x86', 'Æ', newtext)
  newtext = re.sub('\\\\xc3\\\\x87', 'Ç', newtext)
  newtext = re.sub('\\\\xc3\\\\x88', 'È', newtext)
  newtext = re.sub('\\\\xc3\\\\x89', 'É', newtext)
  newtext = re.sub('\\\\xc3\\\\x8a', 'Ê', newtext)
  newtext = re.sub('\\\\xc3\\\\x8b', 'Ë', newtext)
  newtext = re.sub('\\\\xc3\\\\x8c', 'Ì', newtext)
  newtext = re.sub('\\\\xc3\\\\x8d', 'Í', newtext)
  newtext = re.sub('\\\\xc3\\\\x8e', 'Î', newtext)
  newtext = re.sub('\\\\xc3\\\\x8f', 'Ï', newtext)
  newtext = re.sub('\\\\xc3\\\\x90', 'Ð', newtext)
  newtext = re.sub('\\\\xc3\\\\x91', 'Ñ', newtext)
  newtext = re.sub('\\\\xc3\\\\x92', 'Ò', newtext)
  newtext = re.sub('\\\\xc3\\\\x93', 'Ó', newtext)
  newtext = re.sub('\\\\xc3\\\\x94', 'Ô', newtext)
  newtext = re.sub('\\\\xc3\\\\x95', 'Õ', newtext)
  newtext = re.sub('\\\\xc3\\\\x96', 'Ö', newtext)
  newtext = re.sub('\\\\xc3\\\\x97', '×', newtext)
  newtext = re.sub('\\\\xc3\\\\x98', 'Ø', newtext)
  newtext = re.sub('\\\\xc3\\\\x99', 'Ù', newtext)
  newtext = re.sub('\\\\xc3\\\\x9a', 'Ú', newtext)
  newtext = re.sub('\\\\xc3\\\\x9b', 'Û', newtext)
  newtext = re.sub('\\\\xc3\\\\x9c', 'Ü', newtext)
  newtext = re.sub('\\\\xc3\\\\x9d', 'Ý', newtext)
  newtext = re.sub('\\\\xc3\\\\x9e', 'Þ', newtext)
  newtext = re.sub('\\\\xc3\\\\x9f', 'ß', newtext)
  #
  newtext = re.sub('\\\\xc3\\\\xa0', 'à', newtext)
  newtext = re.sub('\\\\xc3\\\\xa1', 'á', newtext)
  newtext = re.sub('\\\\xc3\\\\xa2', 'â', newtext)
  newtext = re.sub('\\\\xc3\\\\xa3', 'ã', newtext)
  newtext = re.sub('\\\\xc3\\\\xa4', 'ä', newtext)
  newtext = re.sub('\\\\xc3\\\\xa5', 'å', newtext)
  newtext = re.sub('\\\\xc3\\\\xa6', 'æ', newtext)
  newtext = re.sub('\\\\xc3\\\\xa7', 'ç', newtext)
  newtext = re.sub('\\\\xc3\\\\xa8', 'è', newtext)
  newtext = re.sub('\\\\xc3\\\\xa9', 'é', newtext)
  newtext = re.sub('\\\\xc3\\\\xaa', 'ê', newtext)
  newtext = re.sub('\\\\xc3\\\\xab', 'ë', newtext)
  newtext = re.sub('\\\\xc3\\\\xac', 'ì', newtext)
  newtext = re.sub('\\\\xc3\\\\xad', 'í', newtext)
  newtext = re.sub('\\\\xc3\\\\xae', 'î', newtext)
  newtext = re.sub('\\\\xc3\\\\xaf', 'ï', newtext)
  newtext = re.sub('\\\\xc3\\\\xb0', 'ð', newtext)
  newtext = re.sub('\\\\xc3\\\\xb1', 'ñ', newtext)
  newtext = re.sub('\\\\xc3\\\\xb2', 'ò', newtext)
  newtext = re.sub('\\\\xc3\\\\xb3', 'ó', newtext)
  newtext = re.sub('\\\\xc3\\\\xb4', 'ô', newtext)
  newtext = re.sub('\\\\xc3\\\\xb5', 'õ', newtext)
  newtext = re.sub('\\\\xc3\\\\xb6', 'ö', newtext)
  newtext = re.sub('\\\\xc3\\\\xb7', '÷', newtext)
  newtext = re.sub('\\\\xc3\\\\xb8', 'ø', newtext)
  newtext = re.sub('\\\\xc3\\\\xb9', 'ù', newtext)
  newtext = re.sub('\\\\xc3\\\\xba', 'ú', newtext)
  newtext = re.sub('\\\\xc3\\\\xbb', 'û', newtext)
  newtext = re.sub('\\\\xc3\\\\xbc', 'ü', newtext)
  newtext = re.sub('\\\\xc3\\\\xbd', 'ý', newtext)
  newtext = re.sub('\\\\xc3\\\\xbe', 'þ', newtext)
  newtext = re.sub('\\\\xc3\\\\xbf', 'ÿ', newtext)
  # incomplete
  newtext = re.sub('\\\\xc4\\\\x9f', 'ğ', newtext)
  newtext = re.sub('\\\\xc4\\\\xb1', 'ı', newtext)
  newtext = re.sub('\\\\xc5\\\\x82', 'ł', newtext)
  newtext = re.sub('\\\\xc5\\\\x93', 'œ', newtext)
  newtext = re.sub('\\\\xcc\\\\x80', '̀', newtext)
  newtext = re.sub('\\\\xcc\\\\x81', '́', newtext)
  newtext = re.sub('\\\\xcc\\\\x88', '̈', newtext)
  # special characters
  newtext = re.sub('\\\\xe2\\\\x80\\\\x93', '-', newtext) # ndash '–'
  newtext = re.sub('\\\\xe2\\\\x80\\\\x94', '-', newtext) # mdash '—'
  newtext = re.sub('\\\\xe2\\\\x80\\\\x98', '‘', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x99', '’', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9a', '‚', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9c', '“', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9d', '”', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9e', '„', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xa0', '†', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xa6', '…', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xa8', ' ', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xaf', ' ', newtext)
  #
  newtext = re.sub('\\\\xe2\\\\x82\\\\xac', '€', newtext)
  #
  newtext = re.sub('\\\\xe2\\\\x84\\\\x97', '℗', newtext)
  newtext = re.sub('\\\\xe2\\\\x84\\\\xa2', '™', newtext)
  #
  newtext = re.sub('\\\\xe2\\\\x93\\\\x85', 'Ⓟ', newtext)
  #
  newtext = re.sub('\\\\xe2\\\\x96\\\\xba', '►', newtext)
  #
  newtext = re.sub('\\\\xe2\\\\x9c\\\\x93', '✓', newtext)
  newtext = re.sub('\\\\xe2\\\\x9c\\\\xa8', '✨', newtext)
  # language representations
  newtext = re.sub('\\\\xce\\\\x95\\\\xce\\\\xbb\\\\xce\\\\xbb\\\\xce\\\\xb7\\\\xce\\\\xbd\\\\xce\\\\xb9\\\\xce\\\\xba\\\\xce\\\\xac', 'Ελληνικά', newtext)
  newtext = re.sub('\\\\xc4\\\\x8de\\\\xc5\\\\xa1tina', 'čeština', newtext)
  newtext = re.sub('\\\\xd1\\\\x80\\\\xd1\\\\x83\\\\xd1\\\\x81\\\\xd1\\\\x81\\\\xd0\\\\xba\\\\xd0\\\\xb8\\\\xd0\\\\xb9', 'русский', newtext)
  newtext = re.sub('\\\\xf0\\\\x9f\\\\x8f\\\\xb7\\\\xef\\\\xb8\\\\x8f', '🏷️', newtext) # some kind of luggage tag?
  # characters in square box
  newtext = re.sub('\\\\xf0\\\\x9f\\\\x87\\\\x..', '[x]', newtext)
  # book stack, ...
  newtext = re.sub('\\\\xf0\\\\x9f\\\\x90\\\\xb0', '[rabbit]', newtext) #🐰
  newtext = re.sub('\\\\xf0\\\\x9f\\\\x91\\\\x8f', '[clap]', newtext)
  newtext = re.sub('\\\\xf0\\\\x9f\\\\x93\\\\x9a', '[books]', newtext)
  newtext = re.sub('\\\\xf0\\\\x9f\\\\x93\\\\xa6', '[box]', newtext) #📦
  newtext = re.sub('\\\\xf0\\\\x9f\\\\x92\\\\x9a', '[green heart]', newtext) #💚
  newtext = re.sub('\\\\xf0\\\\x9f\\\\xa5\\\\x9a', '[egg]', newtext) #🥚
  # some Chinese I can't read nor translate
  newtext = re.sub('\\\\xe9\\\\xbb\\\\x83', '(*)', newtext)
  newtext = re.sub('\\\\xe8\\\\x89\\\\xb2', '(*)', newtext)
  newtext = re.sub('\\\\xe8\\\\x97\\\\x8d', '(*)', newtext)
  # characters not identified yet
  newtext = re.sub('\\\\xef\\\\xb8\\\\x8f', '(*)', newtext) # ??? u+fe0f
  newtext = re.sub('\\\\xef\\\\xbb\\\\xbf', '(*)', newtext) # ??? u+feff
  # Mistake (?) on US server
#  newtext = re.sub('\\\\xe2\\\\x80\\\\x9aÄô', '\'', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9aÑ¢', ',', newtext)
  # check for yet unhandled unicode stuff and show with context
  unknown = re.findall('.{8}\\\\x..\\\\x..\\\\x...{8}', newtext)
  if unknown != [] :
      print('UNKNOWN !!! ' + str(unknown), file = sys.stderr)
  unknown = re.findall('\\\\x..\\\\x..', newtext)
  if unknown != [] :
      print('UNKNOWN !!! ' + str(unknown), file = sys.stderr)
  unknown = re.findall('\\\\x..', newtext)
  if unknown != [] :
      print('UNKNOWN !!! ' + str(unknown), file = sys.stderr)
  # fallback
  newtext = re.sub('\\\\x', '=', newtext)
  # I hate Unicode representations :(
  # why exactly is this necessary?
  newtext = re.sub('\\\\\\\\u', '\\\\u', newtext)
  #
  newtext = re.sub('\\\\u001e', ' ', newtext) # empty box
  newtext = re.sub('\\\\u0026', '&', newtext)
  newtext = re.sub('\\\\u003c', '<', newtext)
  newtext = re.sub('\\\\u003e', '>', newtext)
  newtext = re.sub('\\\\u003c', '<', newtext)
  #
  newtext = re.sub('\\\\u2013', '-', newtext) # ndash '–'
  newtext = re.sub('\\\\u2014', '-', newtext) # mdash '–'
  newtext = re.sub('\\\\u2028', ' ', newtext)
  # check for yet unhandled stuff
  unknown = re.findall('.{8}\\\\u.....{8}', newtext)
  if unknown != [] :
      print('UNKNOWN !!! ' + str(unknown), file = sys.stderr)
  # fallback
  newtext = re.sub('\\\\u', '+', newtext)
  # single quote
  newtext = re.sub('\\\\\'', '\'', newtext)
  newtext = re.sub('\\\\\\\\', '\\\\', newtext)
  return newtext


def cTonies(lang) :
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
  return ctonies


def fixLang(lang) :
  lang = lang.lower()
  if   lang == 'de' :
    lang = 'de-de'
  elif lang == 'en' :
    lang = 'en-gb'
  elif lang == 'fr' :
    lang = 'fr-fr'
  elif lang == 'gb' :
    lang = 'en-gb'
  elif lang == 'us' :
    lang = 'en-us'
  return(lang)


def model8(model) :
  return("        "[len(model) : ] + model)


# known tonies (also creative and demo ones)
orig = {}
orig_url = 'http://gt-blog.de/JSON/tonies.json'
try:
  orig = requests.get(orig_url).json()
  print("  " + str(len(orig)) + " tonies read from web")
except:
  print("ERROR: Cannot load \"tonies.json\" for import of known tonies", file = sys.stderr)
  pass


langs = [
  'de-de',
  'fr-fr',
  'en-gb',
# Europe seems to be a subset of the three before
  'en-eu',
# US/Hongkong have their own server and no creative tonies yet?
  'en-us',
# HongKong only duplicates existing stuff but track lists don't match
#  'en-hk',
]

all_tonies = []
all_models = []

for lang in langs :
  print("Working on language \"" + lang + "\"")

  if lang in [ 'de-de', 'en-gb', 'en-eu', 'fr-fr' ] :
    # European server tonies.com
    url_base = 'https://tonies.com'
    ctonies = cTonies(lang)

    for what in [ 'tonies', ctonies ] :
      if ctonies == '' :
        continue
      print(" Working on \"" + what + "\"")
      tonies = []
      new_tonies = 0
      skipped_tonies = 0
      main_url = '{base}/{lang}/{what}/'.format(base = url_base, lang = lang, what = what)
      r = requests.get(main_url)
      if r.status_code == 200 :
        # search for <script id="__NEXT_DATA__" type="application/json">
        text = str(r.content)
        # strip non-json stuff
        text = re.sub('^.*<script id="__NEXT_DATA__" type="application/json">\s*', '', text)
        text = re.sub('\s*</script.*', '', text)
        text = cleanJson(text)
        all_data = json.loads(text)
        data = all_data['props']['pageProps']['page']['productList']['normalizedProducts']
        for record in data :
          tonie = {}
          if what != 'tonies' : # creative
            tonie['category'] = what
          elif 'genre' in record.keys() :
            tonie['category'] = record['genre']['key']
          if 'images' in record.keys():
            pic = record['images'][1]['src'] # hero-2
            # https://res.cloudinary.com/.../https://...
            tonie['pic'] = re.sub('^https://res.cloudinary.com/.*/http', 'http', pic)
          # model can be 'nn-nnnn' or 'nnnnnnnn' possibly followed by "_xyz..."
          if 'salesId' in record.keys() :
            model = record['salesId']
          else :
            model = record['sku']
          if   re.match('[0-9]{2}-[0-9]{4}', model) :
            model = model[ : 7]
          elif re.match('[0-9]{8}', model) :
            model = model[ : 8]
          elif re.match('[0-9]{7}', model) :
            model = model[ : 7]
          else :
            image = tonie['pic'].split('/')[-1]
            if   re.match('[0-9]{2}-[0-9]{4}', image) :
              model = image[ : 7]
            elif re.match('[0-9]{8}', image) :
              model = image[ : 8]
            elif re.match('[0-9]{7}', image) :
              model = image[ : 7]
            else :
              model = ''
          if model != '' :
            tonie['model'] = model
          tonie['episodes'] = record['name']
          if 'publicationDate' in record.keys() :
            tonie['release'] = str(int(record['publicationDate'] / 1000))
          if 'series' in record.keys() :
            tonie['series'] = record['series']['label']
          else :
            tonie['series'] = record['normalizedCategories'][0]['name']
          tonie['title'] = '{s} - {e}'.format(s = tonie['series'], e = tonie['episodes'])
          if 'lcCC' in record.keys() :
            # warn if other language
            if record['lcCC'].lower() != lang :
              print(" SKIP: " + model8(tonie['model']) + " = " + lang + " \"" + tonie['title'] + "\" - language code " + record['lcCC'], file = warnings)
              skipped_tonies += 1
#              continue
            tonie['language'] = record['lcCC'].lower()
          else :
            tonie['language'] = lang
          # do not use tracks - ranges and unicode!
          if 'ageMin' in record.keys() :
            tonie['age'] = str(abs(record['ageMin']))
          if 'audioSampleUrl' in record.keys() :
            tonie['sample'] = record['audioSampleUrl']
          tonie['url'] = '{base}{path}'.format(base = url_base, path = record['path'])
          # fill in from tonie page
          tonie_url = tonie['url']
          r = requests.get(tonie_url)
          if r.status_code == 200 :
            soup = BeautifulSoup(r.content, 'html.parser')
            # there may be a hint at the model...
            if 'model' not in tonie.keys() :
              section = soup.find_all('section')[0]
              matches = re.findall('data-testextra=.[0-9][0-9-]*[0-9]', str(section))
              if matches != [] :
                model = matches[0][16 : ]
                tonie['model'] = model
            # even creative tonies may be preloaded and have a tracklist
            tracklist = []
            # FIXME: someone please tell me how to find all "list-item-small-title" divs directly...
            divs = soup.find_all('div')
            for div in divs :
              if re.match('<div [^>]*data-testid="list-item-small-title">', str(div)) :
                # remove HTML tags
                track = div.get_text()
                # soften hard space
                re.sub('\xa0', ' ', track)
                # "01 - 01-09 Pups Save the Football Game"
                if re.match("[0-9][0-9] - [0-9][0-9]-[0-9][0-9]", track) :
                  # renumber/replicate entries
                  trk1 = int(track[5 : 7])
                  trk2 = int(track[8 : 10])
                  name = re.sub('^- ', '', track[11 :])
                  for trk in range(trk1, trk2 + 1) :
                    track = f"{trk:02} - " + name
                    # add an index for identically named tracks
                    track = track + " (" + str(trk - trk1 + 1) + ")"
                    tracklist.append(track)
                else :
                  tracklist.append(track)
            tonie['tracks'] = tracklist
          # is this tonie 'model' already known?
          found = False
          if 'model' in tonie.keys() :
            for orig_record in orig :
              if orig_record['model'] == tonie['model'] :
                found = True
                break
          if not found :
            print("ADDED: " + model8(tonie['model']) + " = " + tonie['language'] + " \"" + tonie['title'] + "\"", file = warnings)
            print("ADDED URL: " + tonie['url'], file = warnings)
            new_tonies += 1
          tonies.append(tonie)
      dropped_tonies = 0
      for tonie in tonies:
        model = tonie['model']
        if model not in all_models :
          all_tonies.append(tonie)
          all_models.append(model)
        else :
          print(" DROP: " + model8(tonie['model']) + " = " + tonie['language'] + " \"" + tonie['title'] + "\" - already there", file = warnings)
          dropped_tonies += 1
      summary = "  " + str(len(tonies) - dropped_tonies) + " \"" + what + "\" tonie descriptions stored"
      if new_tonies > 0 :
        summary += ", " + str(new_tonies) + " new ones found"
      if skipped_tonies > 0 :
        summary += ", " + str(skipped_tonies) + " skipped"
      if dropped_tonies > 0 :
        summary += ", " + str(dropped_tonies) + " dropped"
      print(summary)
    # for what
  elif lang == 'en-hk' or \
       lang == 'en-us' :
    if lang == 'en-hk' :
      # Hongkong gets served by the JSelect platform
      url_base = 'https://www.jselect.com'
      oembed = {
                'tonies' : '/en/collections/tonies.oembed',
                #'creative-tonies' : '/en/collections/creative-tonies.oembed'
                # FIXME: no idea yet how to access creatie tonies
               }
    elif lang =='en-us' :
      # US server redirects to Shopify
      url_base = 'https://us.tonies.com'
      oembed = {
                'tonies' : '/collections/content.oembed',
                #'creative-tonies' : '/collections/creative-content.oembed'
                # FIXME: no idea yet how to access creatie tonies
               }
    # both servers provide JSON directly
    for what in oembed.keys() :
      print(" Working on \"" + what + "\"")
      tonies = []
      new_tonies = 0
      skipped_tonies = 0
      main_url = '{base}{path}'.format(base = url_base, path = oembed[what])
      r = requests.get(main_url)
      if r.status_code == 200 :
        text = str(r.content)
        # need to strip b'...' - why?
        text = re.sub('^[^{]*' ,'', text)
        text = re.sub('[^}]*$', '', text)
        text = cleanJson(text)
        all_data = json.loads(text)
        data = all_data['products']
        for record in data :
          tonie = {}
          title = record['title']
          if lang == 'en-hk' :
            title = re.sub('^tonies *', '', title)
          tonie['title'] = title
          # drop accessories
          if   re.match('Toniebox', title) :
            continue
          if   re.match('headphones', title) :
            continue
          model = record['offers'][0]['sku']
          # en-hk uses "T107|10000123", strip prefix
          model = re.sub('^.*\|', '', model)
          tonie['model'] = model
          #tonie['variant'] = str(record['offers'][0]['offer_id'])
          tonie['language'] = lang
          series = ''
          episode = title
          # the US site doesn't have a clear idea of series
          if   re.match('Disney and Pixar ', title) :
            series = 'Disney and Pixar'
            episode = re.sub('Disney and Pixar[ :-]*', '', title)
          elif re.match('Disney .*', title) :
            series = 'Disney'
            episode = re.sub('Disney[ :-]*', '', title)
          elif re.match('.*: .*', title) :
            series = title.split(':')[0]
            episode = re.sub('[^:]+:\s*', '', title)
          elif re.match('.* - .*', title) :
            series = title.split(' -')[0]
            episode = re.sub('[^-]+-\s*', '', title)
          elif re.match('.*- .*', title) :
            series = title.split('-')[0]
            episode = re.sub('[^-]+-\s*', '', title)
          # known series where there is a base episode
          elif re.match('Llama Llama', title) :
            series = 'Llama Llama'
            episode = re.sub('Llama Llama[ :-]*', '', title)
            if episode == '' :
              episode = series
          elif re.match('Peppa Pig', title) :
            series = 'Peppa Pig'
            episode = re.sub('Peppa Pig[ :-]*', '', title)
            if episode == '' :
              episode = series
          elif re.match('Pete the Cat', title) :
            series = 'Pete the Cat'
            episode = re.sub('Pete the Cat[ :-]*', '', title)
          if episode == '' :
            episode = series
          tonie['series'] = series
          tonie['episodes'] = episode
          tonie['url'] = '{base}/products/{handle}'.format(base = url_base, handle = record['product_id'])
          # fill in from tonie page
          tonie_url = tonie['url']
          r = requests.get(tonie_url)
          if r.status_code == 200 :
            soup = BeautifulSoup(r.content, 'html.parser')
            text = str(r.content)
# <audio-player :audio='"https://cdn.shopify.com/s/files/1/0403/5431/6439/files/Pride_AudioClip.mp3?v=1653493870"' :unique-id="4280271041" inline-template>
            audio = re.findall(':audio=[^:]*http[^ ]*\.mp3', text)
            if audio != [] :
              audio = audio[0].split('"')[1].split('?')[0]
              tonie['sample'] = audio
            cdate = re.findall('"created_at":"....-..-..T..:..:..[^"]*"', text)
            if cdate != [] :
              cdate = cdate[0].split('"')[3]
              #tonie['release_date'] = cdate
              # convert date to integer epoch
              tonie['release'] = str(dt.datetime.fromisoformat(cdate).timestamp()).split('.')[0]
            image = re.findall('"http[^"]+[Tt]ransparent.png[^"]*"', text)
            if image != [] :
              image = image[0].split('"')[1]
            else :
              image = re.findall('<meta property="og:image:secure_url" content="[^"]+">', text)
              if image != [] :
                image = '"'.join(image[0].split('"')[3 : -2])
              else :
                image = ''
            if image != '' :
              image = re.sub('(\\\\)*/', '/', image)
              tonie['pic'] = image
#<div id="product-tracklist" class="product-accordion__content rte" aria-hidden="true">
# <p>
#  <strong>Songs and Stories:</strong>
# </p>
# <p>1. Meet Ms. Rainbow</p>
# <p>2. Liliana Llama Celebrates Pride</p>
# <p>3. It's Time for Pride 🎵</p>
# <p>4. Liliana Llama’s Family Day</p>
# <p>5. Piggy Jack’s Pronouns</p>
# <p>6. Little Beau Sheep and His Purple Dress</p>
# <p><span style="background-color:rgb(255,255,255);color:rgb(0,0,0);">Total Run Time: 60 minutes</span></p>
#</div>
            tracklist = []
            divs = soup.find_all('div')
            for div in divs :
              # FIXME: someone please tell me how to find all "product-tracklist" divs directly...
              if re.match('[^>]*id="product-tracklist"', str(div)) :
                for para in div.find_all('p') :
                  match = str(para)
                  if re.match('.*<strong>', match) : # header line
                    continue
                  if re.match('.*Total Run Time', match) : # footer line
                    continue
                  track = para.get_text()
                  # ignore empty lines
                  if re.match('^\s*$', track) :
                    continue
                  # soften hard space
                  re.sub('\xa0', ' ', track)
                  track = re.sub('^Chapter\s*([0-9]+)[:. ]', '\\1 - ', track)
                  # "1-8. xyz"
                  if re.match("[0-9][0-9]*-[0-9][0-9]*.", track) :
                    # renumber/replicate entries
                    trk1 = int(track.split('.')[0].split('-')[0])
                    trk2 = int(track.split('.')[0].split('-')[1])
                    name = re.sub('^[ -]*', '', track.split('.')[1])
                    for trk in range(trk1, trk2 + 1) :
                      track = f"{trk:02} - " + name
                      # add an index for identically named tracks
                      track = track + " (" + str(trk - trk1 + 1) + ")"
                      tracklist.append(track)
                  else :
                    # rename tracks
                    if re.match('[0-9]\.', track) :
                      track = '0' + track
                    if re.match('[0-9][0-9]\.', track) :
                      track = re.sub('^([0-9][0-9])[. ]*', '\\1 - ', track)
                    tracklist.append(track)
            tonie['tracks'] = tracklist
          # is this tonie 'model' already known?
          found = False
          if 'model' in tonie.keys() :
            for orig_record in orig :
              if orig_record['model'] == tonie['model'] :
                found = True
                break
          if not found :
            print("ADDED: " + model8(tonie['model']) + " = " + tonie['language'] + " \"" + tonie['title'] + "\"", file = warnings)
            new_tonies += 1
          tonies.append(tonie)
      dropped_tonies = 0
      for tonie in tonies:
        model = tonie['model']
        if model not in all_models :
          all_tonies.append(tonie)
          all_models.append(model)
        else :
          print(" DROP: " + model8(tonie['model']) + " = " + tonie['language'] + " \"" + tonie['title'] + "\" - already there", file = warnings)
          dropped_tonies += 1
      summary = "  " + str(len(tonies) - dropped_tonies) + " \"" + what + "\" tonie descriptions stored"
      if new_tonies > 0 :
        summary += ", " + str(new_tonies) + " new ones found"
      if skipped_tonies > 0 :
        summary += ", " + str(skipped_tonies) + " skipped"
      if dropped_tonies > 0 :
        summary += ", " + str(dropped_tonies) + " dropped"
      print(summary)
    # for what
  # if lang
# for lang

print("Adding/merging old tonies")
# add missing tonies from original file
extra_tonies = []
for orig_tonie in orig :
  tonie = orig_tonie
  model = orig_tonie['model']
  if not model in all_models :
    extra_tonies.append(tonie)
for tonie in extra_tonies :
  # remove meaningless number
  tonie.pop('no', None)
  # fix language
  lang = fixLang(tonie['language'])
  tonie['language'] = lang
  all_tonies.append(tonie)
  all_models.append(tonie['model'])
print("  " + str(len(extra_tonies)) + " tonies added back from original list")

print("Filling in from original list")
for tonie in all_tonies :
  # fill in from original json - identify record by "model"
  # tonie['audio_id']
  # tonie['hash']
  # tonie['category']
  # tonie['release']
  # CAVEAT: there may be multiple records for the same model - use first hit
  if 'model' in tonie.keys() :
    for orig_tonie in orig :
      if orig_tonie['model'] == tonie['model'] :
        for key in [
                    'audio_id',
                    'hash',
                    'category',
                    'release',
                    ] :
          if key not in tonie.keys() and \
             key in orig_tonie.keys() :
            tonie[key] = orig_tonie[key]
        break
  else :
    print(" WARN: " + "???????? = " + tonie['language'] + " \"" + tonie['title'] + "\" - no model code", file = warnings)

print("More required fields")
for tonie in all_tonies :
  if 'release' not in tonie.keys() :
    tonie['release'] = "0"
  if 'audio_id' not in tonie.keys() :
    tonie['audio_id'] = []
  if 'hash' not in tonie.keys() :
    tonie['hash'] = []


# attempt to fill in tracks only from tonies.club
special = {
  ord('/'): '', ord('('): '', ord(')'): '',
  ord(','): ' ', ord('.'): ' ',
  ord('!'): '', ord('?'): '', ord('%'): '', ord('’'): '', ord('&'): '', ord(':'): '',
  ord('('): '', ord(')'): '',
  ord('–'): '-',
}
umlaut1 = {
  ord('ä'): 'a', ord('ö'): 'o', ord('ü'): 'u', ord('ß'): 'ss',
}
umlaut2 = {
  ord('ä'): 'ae', ord('ö'): 'oe', ord('ü'): 'ue', ord('ß'): 'ss',
}
blank = {
  ord(' '): '-'
}
# tonies known at tonies.club - track lists are here
club_lookup = {}
try :
  with open ("tc-tonies.json","r") as f :
    data = f.read()
    f.close()
    club = json.loads(data)
  for tonie in club :
    if 'url_invalid' not in tonie.keys() and \
       'tracks' in tonie.keys() :
      if tonie['tracks'] != "" :
        club_lookup[tonie['url']] = tonie
  print("  " + str(len(club_lookup)) + " tonie tracks lookup records from tonies.club loaded")
except :
  print("ERROR: Cannot open \"tc-tonies.json\" for import of known track lists", file = sys.stderr)
club_fill = 0
for tonie in all_tonies :
  if 'tracks' not in tonie.keys() or \
     tonie['tracks'] == [] :
    pass
  else :
    # no need to fill in tracks
    continue
  # attempt with club data
  if 'url' in tonie.keys() :
    url = tonie['url']
    # skip creative tonies completely? at least don't complain
    if re.match('.*/' + cTonies(tonie['language']) + '/', url) :
      continue
#    print(" TRKS: \"" + tonie['title'] + "\" has no track list yet, check \"" + url + "\"")
    if url in club_lookup.keys():
      tonie['tracks'] = club_lookup[url]['tracks']
      club_fill += 1
      print(" CLUB: URL \"" + url + "\" for tonie \"" + tonie['title'] + "\" found", file = warnings)
      continue
  # FIXME: tonie no longer listed / URL unknown
  # pass-through any failed attempt above to here?
  title = tonie['title']
  lang = fixLang(tonie['language'])
  tonie['language'] = lang
  if not re.match('.* - .*', title) :
    continue
  for what in [
               'tonies',
               cTonies(lang)
               ] :
    if what == '' :
      continue
    # split title at ' - '
    series  = title.lower().split(' - ')[0]
    episode = title[3 + len(series) : ].lower()
    for umlaut in [umlaut1, umlaut2] :
      newtitle = re.sub('--+', '-', series.translate(special).translate(umlaut).translate(blank)) + '/' + \
                 re.sub('--+', '-', episode.translate(special).translate(umlaut).translate(blank))
      url = 'https://tonies.com/{lang}/{what}/{title}/'.format(lang = lang, what = what, title = newtitle)
      if url in club_lookup.keys():
        tonie['tracks'] = club_lookup[url]['tracks']
        club_fill += 1
        print(" CLUB: URL \"" + url + "\" for tonie \"" + tonie['title'] + "\" found", file = warnings)
        continue
    #for umlaut
  #for what
#  print(" TRKS: \"" + tonie['title'] + "\" has no track list", file = warnings)
#for tonie
print("  " + str(club_fill) + " track lists copied from tonies.club")


print("  " + str(len(all_tonies)) + " tonie descriptions found")


print("Sorting output by 'model', 'language' and 'title'")
models = []
for tonie in all_tonies :
  if 'model' in tonie.keys() :
    models.append(tonie['model'] + tonie['language'] + tonie['title'])
  else :
    models.append("00-0000" + tonie['language'] + tonie['title'])
indexes = np.argsort(models)
sorted_tonies = []
sorted_models = []
for index in indexes :
  sorted_tonies.append(all_tonies[index])
  sorted_models.append(all_models[index])
all_tonies = sorted_tonies
all_models = sorted_models


## some final brush-up would make list look nicer, but naming is inconsistent
#for tonie in all_tonies :
#      if tonie['series'] == "Kreativ-Tonies" :
#        tonie['series'] = "Kreativ-Tonie" # 
#        tonie['title'] = tonie['series'] + ' - ' + tonie['episodes']
#      if re.match('Kreativ-Tonie ', tonie['episodes']) :
#        tonie['series'] = "Kreativ-Tonie"
#        tonie['episodes'] = tonie['episodes'][14 :]
#        tonie['title'] = tonie['series'] + ' - ' + tonie['episodes']


print("Check for multiple AudioIDs and Hashes")
issue_tonies = 0
for tonie in all_tonies :
  if 'audio_id' not in tonie.keys() or \
     'hash' not in tonie.keys() :
#    print(" WARN: " + model8(tonie['model']) + " = " + tonie['language'] + " \"" + tonie['title'] + "\" has no AudioID/Hash identity, fixing", file = warnings)
#    tonie['audio_id'] = [ "1" ]
#    tonie['hash'] = []
    issue_tonies += 1
    pass
  else :
    if len(tonie['audio_id']) > 1 or \
       len(tonie['hash']) > 1 :
      if len(tonie['audio_id']) > 1 :
        #print(tonie['model'] + " = " + tonie['language'] + " \"" + tonie['title'] + "\" has " + str(len(tonie['audio_id'])) + " AudioId identities", file = warnings)
        pass
      if len(tonie['hash']) > 1 :
        #print(tonie['model'] + " = " + tonie['language'] + " \"" + tonie['title'] + "\" has " + str(len(tonie['hash']))     + "    Hash identities", file = warnings)
        pass
      if len(tonie['audio_id']) != len(tonie['hash']) :
        print(" WARN: " + model8(tonie['model']) + " = " + tonie['language'] + " \"" + tonie['title'] + "\" has " \
              + str(len(tonie['audio_id'])) + " AudioId and " \
              + str(len(tonie['hash']))     + " Hash identities", file = warnings)
        pass
      issue_tonies += 1
    # some tonies have an audioID of "1" :(
    for id in tonie['audio_id'] :
      if int(id) < 1000000000 or \
         int(id) > 2147483647 : # before 2001 or after 2038
#        print(tonie['model'] + " = " + tonie['language'] + " \"" + tonie['title'] + "\" has invalid AudioID " + id, file = warnings)
#        issue_tonies += 1
        pass
# ... more to come?
print("  " + str(issue_tonies) + " possible issues identified")


# raw data - pass through json_pp
with open('{base}.raw.json'.format(base = output_base), 'w') as f :
  json.dump(all_tonies, f)
  f.close()


# list of tonies (to find dupes etc.)
list = ''
for tonie in all_tonies :
  line = '{model}\t{lang}\t{title}\n'.format(model = model8(tonie['model']), lang = tonie['language'], title = tonie['title'])
  list += line
with open('{base}.list'.format(base = output_base), 'w') as f :
  f.write(list)
  f.close()


if warnings != sys.stderr :
  warnings.close()
