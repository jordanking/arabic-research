#!/usr/bin/env python
# coding: utf-8

# ARAPY_PATH = "/home/jordan/Documents/Projects/"
# WORKING_DIRECTORY = "/home/jordan/Documents/Projects/arabic-research/temp"
# WIKI_FILE = WORKING_DIRECTORY+"/0-wiki/arwiki-20150901-pages-articles.xml"
# PARSE_FILE = WORKING_DIRECTORY+"/1-parsed/parsed.txt"

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
from constants import ARAPY_PATH, WORKING_DIRECTORY, WIKI_FILE, PARSE_FILE
import logging
import sys
sys.path.insert(0,ARAPY_PATH)
from arapy.arwiki import parse_arwiki_dump

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
logging.info("Parsing dump.")
parse_arwiki_dump(WIKI_FILE, PARSE_FILE, split_at_punc=True, remove_non_arabic=True)
logging.info("Done!")