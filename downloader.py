#!/usr/bin/env python

# https://search.creativecommons.org/

import urllib

for line in open('urls.txt'):
	with open('input/' + line.split('/')[-1], 'wb') as image:
		image.write(urllib.urlopen(line).read())