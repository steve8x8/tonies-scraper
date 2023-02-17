#!/usr/bin/python3

# scraper for tonies known by tonies.club
# to potentially fill in data missing on the original web page


from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import json
import numpy as np
import pandas as pd
import re
import requests
import sys

output_base = 'tc-tonies'

# stderr redirect
#warnings = sys.stderr
warnings = open('{base}.warn'.format(base = output_base), "w")


special_char_map = {}

# clean embedded JSON code
def cleanJson(text) :
  newtext = str(text)
  # umlauts etc
  newtext = re.sub('&#39;', '\'', newtext)
  newtext = re.sub('&amp;', '&', newtext)

  newtext = re.sub('\\\\\\\\', '\\\\', newtext)
  newtext = re.sub('\\\\x3c', '<', newtext)
  newtext = re.sub('\\\\x3e', '>', newtext)
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
  newtext = re.sub('\xcc\x88', '̈', newtext)
  newtext = re.sub('a¨',  'ä', newtext)
  newtext = re.sub('o¨',  'ö', newtext)
  newtext = re.sub('u¨',  'ü', newtext)
  newtext = re.sub('A¨',  'Ä', newtext)
  newtext = re.sub('O¨',  'Ö', newtext)
  newtext = re.sub('U¨',  'Ü', newtext)
  # incomplete
  newtext = re.sub('\\\\xc4\\\\x9f', 'ğ', newtext)
  newtext = re.sub('\\\\xc4\\\\xb1', 'ı', newtext)
  newtext = re.sub('\\\\xc5\\\\x82', 'ł', newtext)
  newtext = re.sub('\\\\xc5\\\\x93', 'œ', newtext)
  newtext = re.sub('\\\\xcc\\\\x80', '\'', newtext) # '̀'
  newtext = re.sub('\\\\xcc\\\\x81', '\'', newtext) # '́'
  newtext = re.sub('\\\\xcc\\\\x88', '"', newtext)  # '̈'
  newtext = re.sub('̀', '\'', newtext)
  newtext = re.sub('́', '\'', newtext)
  newtext = re.sub('`', '\'', newtext)
  newtext = re.sub('’', '\'', newtext)
  # special characters
  newtext = re.sub('\\\\xe2\\\\x80\\\\x93', '-', newtext) # ndash '–'
  newtext = re.sub('\\\\xe2\\\\x80\\\\x94', '-', newtext) # mdash '—'
  newtext = re.sub('\\\\xe2\\\\x80\\\\x98', '\'', newtext) # '‘'
  newtext = re.sub('\\\\xe2\\\\x80\\\\x99', '\'', newtext) # '’'
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9c', '“', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9d', '”', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\x9e', '„', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xa0', '†', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xa6', '…', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xa8', ' ', newtext)
  newtext = re.sub('\\\\xe2\\\\x80\\\\xaf', ' ', newtext)
  newtext = re.sub('–', '-', newtext)
  newtext = re.sub('—', '-', newtext)
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
  #
  newtext = re.sub('\\\\xef\\\\xb8\\\\x8f', '(*)', newtext) # ??? u+fe0f
  newtext = re.sub('\\\\xef\\\\xbb\\\\xbf', '(*)', newtext) # ??? u+feff
  # language representations
  newtext = re.sub('\\\\xce\\\\x95\\\\xce\\\\xbb\\\\xce\\\\xbb\\\\xce\\\\xb7\\\\xce\\\\xbd\\\\xce\\\\xb9\\\\xce\\\\xba\\\\xce\\\\xac', 'Ελληνικά', newtext)
  newtext = re.sub('\\\\xc4\\\\x8de\\\\xc5\\\\xa1tina', 'čeština', newtext)
  newtext = re.sub('\\\\xd1\\\\x80\\\\xd1\\\\x83\\\\xd1\\\\x81\\\\xd1\\\\x81\\\\xd0\\\\xba\\\\xd0\\\\xb8\\\\xd0\\\\xb9', 'русский', newtext)
  # Chinese
  newtext = re.sub('\\\\xe9\\\\xbb\\\\x83', '(*)', newtext)
  newtext = re.sub('\\\\xe8\\\\x89\\\\xb2', '(*)', newtext)
  newtext = re.sub('\\\\xe8\\\\x97\\\\x8d', '(*)', newtext)
  # check for yet unhandled unicode stuff
  unknown = re.findall('\\\\x..\\\\x..\\\\x..', newtext)
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
  unknown = re.findall('\\\\u....', newtext)
  if unknown != [] :
      print('UNKNOWN !!! ' + str(unknown), file = sys.stderr)
  # fallback
  newtext = re.sub('\\\\u', '+', newtext)
  # single quote
  newtext = re.sub('\\\\\'', '\'', newtext)
  newtext = re.sub('\\\\\\\\', '\\\\', newtext)

  return newtext


url_base = 'https://tonies.club'
# unlike tonies.com, tonies.club uses real "pages", no json/ajax magic

# get number of pages
r = requests.get(url_base + '/tonie/all')
if r.status_code != 200 :
  print("Failed to load start page!", file = sys.stderr)
  quit()
pages = 1
soup = BeautifulSoup(r.content, 'html.parser')
href_all = soup.find_all('a', href=True)
request_urls = [href['href'] for href in href_all]
for url in request_urls:
  if re.match('^/tonie/all\?page=', url):
    p = url[16:]
    if int(p) > pages:
      pages = int(p)
print(str(pages) + " pages to be crawled")

# now get all urls from all pages
tonie_urls = []
for page in range(1, pages + 1):
  r = requests.get(url_base + '/tonie/all?page=' + str(page))
  if r.status_code != 200 :
    print("Failed to load page {page}".format(page = page), file = sys.stderr)
    continue
  soup = BeautifulSoup(r.content, 'html.parser')
  hrefs = soup.find_all('a', href=True)
  urls = [href['href'] for href in hrefs]
  for url in urls :
    # https://tonies.club/tonie/st.-pauli-rabauken/entscheidung-am-millerntor
    url = re.sub('\.', '', url)
    # regular tonies have a "series" and "episode"
    if re.match('^/tonie/.*/.*', url) :
      if url not in tonie_urls:
        tonie_urls.append(url)

# now get individual tonies and extract information
tonies = []
for tonie_url in tonie_urls:
  full_url = url_base + tonie_url
  tonie = {}
  r = requests.get(full_url)
  if r.status_code != 200 :
    print("Failed to load tonie from {tonie}".format(tonie = full_url), file = warnings)
    continue
  tonie['club_url'] = full_url
  soup = BeautifulSoup(r.content, 'html.parser')
  text = cleanJson(r.content)

#    <meta property="og:title"       content="Die Biene Maja - Majas Geburt" />
  title = re.sub(r'.*"og:title"\s*content="', '', text)
  title = re.sub(r'"\s*/>.*', '', title)
  if re.sub('\s-.*', '', title) == '^US Tonie - ' :
    tonie['language'] = 'en-us'
    title = title[11 : ]
  tonie['title'] = title
  tonie['series'] = re.sub('\s-.*', '', title)
  tonie['episodes'] = re.sub('^[^-]+-\s*', '', title)
  # special case:
  if title == "Bitte nicht öffnen - Bissig! - Bissig!" :
    tonie['series'] = "Bitte nicht öffnen - Bissig!"
    tonie['episodes'] = "Bissig!"

#<div class="carousel-inner">
#<div class="carousel-item active">
#<img class="img-fluid mx-auto d-block" src="/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ2dCIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--ef5eac4cec5c4bafb560e5216dfdfaa82e2430ed/tonie103_1.jpg"/>
#</div>
#<div class="carousel-item">
#<img class="img-fluid mx-auto d-block" src="/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ2tCIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--2dd5447270d58660619b7b44aa391b968e293f72/tonie103_2.jpg"/>
#</div>
#<div class="carousel-item">
#<img class="img-fluid mx-auto d-block" src="/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ29CIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--3bc45f4c90634139174c44c5c090e2f44addc81a/tonie103_3.jpg"/>
#</div>
#</div>
  for div in soup.find_all('div') :
    if not re.match('.*class="carousel-inner"', str(div)) :
      continue
    images = []
    for img in div.find_all('img') :
      image = url_base + img['src']
      images.append(image)
    pic = ''
    if images != [] :
      if len(images) > 1 :
        pic = images[1]
      else :
        pic = images[0]
    if pic != '' :
      tonie['pic'] = pic

#<div aria-labelledby="headingTwo" class="collapse" data-parent="#TonieContent" id="collapseTwo">
#<div class="card-body">
#	Wunderbare Pferde 1<br/>Wunderbare Pferde 2<br/>Wunderbare Pferde 3<br/>Wunderbare Pferde 4<br/>Wunderbare Pferde 5<br/>Wunderbare Pferde 6<br/>Wunderbare Pferde 7<br/>Wunderbare Pferde 8<br/>Wunderbare Pferde 9<br/>Wunderbare Pferde 10<br/>Wunderbare Pferde 11<br/>Wunderbare Pferde 12<br/>Wunderbare Pferde 13<br/>Wunderbare Pferde 14<br/>Wunderbare Pferde 15<br/>Wunderbare Pferde 16<br/>Wunderbare Pferde 17<br/>Reitervolk Mongolen 1<br/>Reitervolk Mongolen 2<br/>Reitervolk Mongolen 3<br/>Reitervolk Mongolen 4<br/>Reitervolk Mongolen 5<br/>Reitervolk Mongolen 6<br/>Reitervolk Mongolen 7<br/>Reitervolk Mongolen 8<br/>Reitervolk Mongolen 9<br/>Reitervolk Mongolen 10<br/>Reitervolk Mongolen 11<br/>Reitervolk Mongolen 12<br/>Reitervolk Mongolen 13<br/>Reitervolk Mongolen 14<br/>Reitervolk Mongolen 15
#    </div>
#</div>
  titlelist = soup.find_all('div', id="collapseTwo")
  if titlelist != [] :
    tracks = []
    tracklist = str(titlelist[0]).translate(special_char_map)
    # remove heading lines
    tracklist = re.sub('\s*<div[^>]*id="collapseTwo"[^>]*>\s*', '', tracklist)
    tracklist = re.sub('\s*<div[^>]*class="card-body"[^>]*>\s*', '', tracklist)
    # do not reemove trailing lines yet
    #tracklist = re.sub('\s*</div>\s*', '', tracklist)
    # pages may use <p> or <div> brackets in addition to "regular" <br/>
    tracklist = re.sub('</div>', '<br/>', tracklist)
    tracklist = re.sub('</p>', '<br/>', tracklist)
    # just in case... as we can't split() on a regex
    tracklist = re.sub('<br>', '<br/>', tracklist)
    tracklist = re.sub('<br\s[^>]*>', '<br/>', tracklist)
    # there are also some stray linefeeds
    tracklist = re.sub('\s*\n\s*', '<br/>', tracklist)
    # now process individual track entries
    trk = 0
    for trackline in tracklist.split('<br/>') :
      if re.match('.*<strong>.*</strong>', trackline) :
        continue
      if re.match('.*Total Run Time', trackline) :
        continue

      # remove remaining HTML code
      trackline = re.sub('\s*<[^>]*>\s*', '', trackline)
      # remove surrounding white space
      trackline = re.sub('^\s+', '', trackline)
      trackline = re.sub('\s+$', '', trackline)
      trackline = re.sub('^\.', '', trackline)

      trackline = cleanJson(trackline)

      # ignore now-empty lines
      if re.match('^\s*$', trackline) :
        continue

      # a few known bad entries...
      if trackline == "1" :
        continue
      # Das kleine Gespenst 2022
      if re.match('- [0-9][0-9]', trackline) :
        trackline = "01 " + trackline
      if re.match('– [0-9]+\.: ', trackline) :
        trackline = "1 - " + re.sub('- ([0-9]+)\.: ', '\\1: ', trackline)
      # Mickey Holiday and others - song???
      trackline = re.sub(' *ðŸŽµ *', ' (SONG)', trackline)

      # number of tracks with possibly identical track title
      count = 1
      trackname = trackline
      match = ''

      # track numbering is handled inconsistently on the server
      if   not re.match('[0-9]', trackline) :
        pass
      # nn - 10 mal 10
      elif re.match('[0-9][0-9] - 10 mal 10', trackline) :
        match = re.match('[0-9][0-9] - ', trackline).group()
        trackname = trackline[5 : ]
      # nn - nn
      elif re.match('[0-9][0-9] - [0-9][0-9]:? +', trackline) :
        match = re.match('[0-9][0-9] - [0-9][0-9]:? +', trackline).group()
        trackname = re.sub('^[0-9]+ - [0-9]+[ :-]+', '', trackline)
        trk1 = int(trackline[0 : 2])
        trk2 = int(trackline[5 : 7])
        count = trk2 - trk1 + 1
      # n - [n]n
      elif re.match('[1-9] - [1-9]?[0-9]:? +', trackline) :
        match = re.match('[1-9] - [1-9]?[0-9]:? +', trackline).group()
        trackname = re.sub('^[1-9] - [0-9]+[ :-]+', '', trackline)
        trk1 = int(trackline[0 : 1])
        trk2 = int(re.sub('^[1-9] - ([0-9]+)[ :-]+.*', '\\1', trackline))
        count = trk2 - trk1 + 1
      # [n]n-[n]n -
      elif re.match('[0-9]+-[0-9]+ - ', trackline) :
        match = re.match('[0-9]+-[0-9]+ - ', trackline).group()
        trackname = re.sub('^[0-9]+-[0-9]+ - +', '', trackline)
        trk1 = int(trackline.split('-')[0])
        trk2 = int(re.sub('^([0-9]+)-([0-9]+) - .*', '\\2', trackline))
        count = trk2 - trk1 + 1
      # [n]n-[n]n
      elif re.match('[0-9]+-[0-9]+ ', trackline) :
        match = re.match('[0-9]+-[0-9]+ ', trackline).group()
        trackname = re.sub('^[0-9]+-[0-9]+ +', '', trackline)
        trk1 = int(trackline.split('-')[0])
        trk2 = int(re.sub('^([0-9]+)-([0-9]+) .*', '\\2', trackline))
        count = trk2 - trk1 + 1
      # "1 – 12: 100% Wolf"
      elif re.match('[0-9]+ bis [0-9]+: ', trackline) :
        match = re.match('[0-9]+ bis [0-9]+: ', trackline).group()
        trackname = re.sub('[0-9]+ bis [0-9]+: +', '', trackline)
        trk1 = int(trackline[0 : 2])
        trk2 = int(re.sub('([0-9]+).*', '\\1', trackline.split(' bis ')[1]))
        count = trk2 - trk1 + 1
      elif re.match('[0-9]+ bis [0-9]+ *- ', trackline) :
        match = re.match('[0-9]+ bis [0-9]+ *- ', trackline).group()
        trackname = re.sub('[0-9]+ bis [0-9]+ *- ', '', trackline)
        trk1 = int(trackline[0 : 2])
        trk2 = int(re.sub('([0-9]+).*', '\\1', trackline.split(' bis ')[1]))
        count = trk2 - trk1 + 1
      # "43 Kapitel: Bitte nicht öffnen – Bissig!"
      elif re.match('[0-9][0-9] Kapitel', trackline) :
        match = re.match('[0-9]+ Kapitel', trackline).group()
        trackname = re.sub('[0-9]+ Kapitel: ', '', trackline)
        count = 43
      elif re.match('[0-9]+ ?-', trackline) :
        match = re.match('[0-9]+ ?-', trackline).group()
        trackname = re.sub('[0-9]+ ?- *' , '', trackline)
      elif re.match('[0-9][0-9] ', trackline) :
        match = re.match('[0-9][0-9] ', trackline).group()
        trackname = trackline[3 : ]
      elif re.match('[0-9]+\. Satz', trackline) :
        match = re.match('[0-9]+\. Satz', trackline).group()
        pass
      elif re.match('[0-9]+\.', trackline) :
        match = re.match('[0-9]+\.', trackline).group()
        trackname = re.sub('^[0-9]+\. *', '', trackname)
      elif re.match('[0-9]+: ', trackline) :
        match = re.match('[0-9]+: ', trackline).group()
        trackname = re.sub('^[0-9]+: *', '', trackname)

      trackname = re.sub('^\.', '', trackname)
      trackname = re.sub('\s*\(env. [0-9]+ min\)', '', trackname)

      # multiply track titles if there's a range, (number tracks)
      for tmp in range(1, count + 1) :
        trk += 1
        track = f"{trk:02} - " + trackname
#        track = trackname
        # append counter if and only if multiple tracks with same name
        if count > 1 :
          track += " (" + str(tmp) + ")"
        tracks.append(track)
    # for trackline
    if tracks != [] :
      tonie['tracks'] = tracks
  # if titlelist

#    <a href="https://tonies.com/de-de/tonies/die-biene-maja/majas-geburt/" class="link" target="_blank"><i class="fas fa-external-link-alt"></i>&nbsp;im Tonie Shop ansehen</a>
  hrefs = soup.find_all('a', href=True)
  for href in hrefs :
    if not re.match('.*im Tonie Shop ansehen.*', str(href)) :
      continue
    ext_url = href['href']
    ext_url = re.sub('/tonies.de/shop/', '/tonies.com/de-de/', ext_url)
    ext_url = re.sub('/tonies.com/de-de/shop/', '/tonies.com/de-de/', ext_url)
    tonie['url'] = ext_url
    # check validity of ext_url
    try :
        r = requests.get(ext_url)
      # may be invalid or outdated - not all tonies are kept there
        if r.status_code != 200 :
          tonie['url_invalid'] = 1
    except :
          tonie['url_invalid'] = 1
    if 'url_invalid' in tonie.keys() :
          print("Failed to open URL \"" + ext_url + "\" for \"" + tonie['title'] + "\"", file = warnings)

  if tonie != {} :
    tonies.append(tonie)


# sort by "club_url" (?)
club_urls = []
for tonie in tonies :
  if 'club_url' in tonie.keys() :
    club_urls.append(tonie['club_url'])
  else:
    club_urls.append('')
indexes = np.argsort(club_urls)
sorted_tonies = []
for index in indexes :
  sorted_tonies.append(tonies[index])
tonies = sorted_tonies


with open('{base}.raw.json'.format(base = output_base), 'w') as f:
    json.dump(tonies, f)


if warnings != sys.stderr :
  warnings.close()
