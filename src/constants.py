#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function

ARAPY_PATH = "/home/jordan/Documents/Projects/"
WORKING_DIRECTORY = "/home/jordan/Documents/Projects/arabic-research/temp"

WIKI_FILE = WORKING_DIRECTORY+"/0-wiki/arwiki-20150901-pages-articles.xml"
PARSE_FILE = WORKING_DIRECTORY+"/1-parsed/parsed.txt"
LEMMA_FILE = WORKING_DIRECTORY+"/2-preprocessed/lemmas.txt"
TOKEN_FILE = WORKING_DIRECTORY+"/2-preprocessed/tokens.txt"
POS_FILE = WORKING_DIRECTORY+"/2-preprocessed/pos.txt"
CONTROL_FILE = WORKING_DIRECTORY+"/2-preprocessed/control.txt"
PREPROCESSED_DIR = WORKING_DIRECTORY+"/2-preprocessed"
NORMALIZED_DIR = WORKING_DIRECTORY+"/3-normalized"
EMBEDDING_DIR = WORKING_DIRECTORY+"/4-embeddings"
RESULTS_DIR = WORKING_DIRECTORY+"/5-semantic_results"

TASKS = ['/home/jordan/Documents/Projects/arabic-research/semantic_tasks/mine/similarity_task_merged.csv',
         '/home/jordan/Documents/Projects/arabic-research/semantic_tasks/others/WS353_ar.csv',
         '/home/jordan/Documents/Projects/arabic-research/semantic_tasks/others/WS353_en.csv']

AR_SIM_OUTPUT_FILE = RESULTS_DIR+'/ar_similiarity_task_results.csv'
EN_SIM_OUTPUT_FILE = RESULTS_DIR+'/en_similiarity_task_results.csv'

IN_HEADER = ['Word 1', 'Word 2', 'Similarity']
OUT_HEADER = ['Embedding File', 'MSE', 'Accuracy', 'Hit_Percent', 'Correlation']