#!/usr/bin/python

sublime_path = '/home/zhomart/.sublime_text'
cache_path = 'cache'

import os
import httplib, urllib
import re
from sys import stdout
import shutil

cache_path = os.path.join(os.getcwd(), cache_path)

print 'finding last version'

conn = httplib.HTTPConnection("www.sublimetext.com")
conn.request("GET", "/dev")
r = conn.getresponse()

if r.status != 200:
  print "I can't update (%s)" % r.reason
  exit()

reg = re.compile(r"^.*<a href=\"http://(.*/Sublime Text 2 Build (\d{4}) x64.tar.bz2)\">Linux 64 bit</a>.*$", re.M | re.S)
match = reg.match(r.read())

url = match.group(1)
version = match.group(2)

print 'last version is %s' % version

if not os.path.exists(cache_path):
  os.makedirs(cache_path)

url_encoded = "http://"+ urllib.pathname2url(url)
url_file = urllib.urlopen(url_encoded)

size = int(url_file.headers['Content-Length']) # bytes

filename = 'sublime_text_%s.tag.bz2' % version
file_path = os.path.join(cache_path, filename)

# if not exists or not downloaded
# download file
if not os.path.exists(file_path) or os.path.getsize(file_path) != size:
  print 'downloading file "%s"' % url
  f = open(file_path, 'w')
  downloaded = 0
  while downloaded < size:
    tmp = url_file.read(2048)
    downloaded += len(tmp)
    f.write(tmp)
    stdout.write("\r%.2d%%" % (downloaded*100.0/size))
    stdout.flush()
  f.close()
  print '\nsaved to: %s' % file_path
else:
  print 'already downloaded: %s' % file_path

new_path = os.path.join(sublime_path, filename)

print 'updating...'

tmp_directory = 'Sublime Text 2'

shutil.rmtree("%s", os.path.join(cache_path, tmp_directory))

os.system('cd %s; tar -xf %s' % (cache_path, filename))

os.chdir(os.path.join(cache_path, tmp_directory))

if not os.path.exists(sublime_path):
  os.makedirs(sublime_path)

os.system('cp -r * %s' % sublime_path)

print 'done!'

print 'please restart your sublime text'
