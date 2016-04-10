#!/usr/bin/env python
# coding: utf-8

# ARAPY_PATH = "/home/jordan/Documents/Projects/"
# WORKING_DIRECTORY = "/home/jordan/Documents/Projects/arabic-research/temp"
# PARSE_FILE = WORKING_DIRECTORY+"/1-parsed/parsed.txt"
# LEMMA_FILE = WORKING_DIRECTORY+"/2-preprocessed/lemmas.txt"
# TOKEN_FILE = WORKING_DIRECTORY+"/2-preprocessed/tokens.txt"
# POS_FILE = WORKING_DIRECTORY+"/2-preprocessed/pos.txt"
# CONTROL_FILE = WORKING_DIRECTORY+"/2-preprocessed/control.txt"

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
from constants import ARAPY_PATH, WORKING_DIRECTORY, PARSE_FILE
from constants import LEMMA_FILE, TOKEN_FILE, POS_FILE, CONTROL_FILE
import sys
sys.path.insert(0,ARAPY_PATH)
from arapy.madamira import transform_sentence_file
import shutil
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
logging.info("Obtaining Lemmas, POS, and Tokens")
transform_sentence_file(PARSE_FILE, 
                        lemmaout=LEMMA_FILE,
                        tokenout=TOKEN_FILE,
                        posout=POS_FILE,
                        lemmas=True,
                        pos=True,
                        tokens=True)
shutil.copyfile(PARSE_FILE, CONTROL_FILE)
logging.info("Done!")