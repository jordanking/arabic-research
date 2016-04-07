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
EMBEDDING_DIR = WORKING_DIRECTORY+"/4-1-embeddings"
RESULTS_DIR = WORKING_DIRECTORY+"/5-semantic_results"

TASKS = ['/home/jordan/Documents/Projects/arabic-research/semantic_tasks/mine/similarity_task_merged.csv',
         '/home/jordan/Documents/Projects/arabic-research/semantic_tasks/others/WS353_ar.csv',
         '/home/jordan/Documents/Projects/arabic-research/semantic_tasks/others/WS353_en.csv',
         '/home/jordan/Documents/Projects/arabic-research/semantic_tasks/mine/similarity_task_multi_vote.csv',
         '/home/jordan/Documents/Projects/arabic-research/semantic_tasks/mine/similarity_task_4_votes.csv']

AR_SIM_OUTPUT_FILES = [RESULTS_DIR+'/ar_similiarity_task_results.csv',
                       RESULTS_DIR+'/ar_similiarity_task_results_ws353.csv',
                       'english placeholder',
                       RESULTS_DIR+'/ar_similiarity_task_multi_results.csv',
                       RESULTS_DIR+'/ar_similiarity_task_4_votes_results.csv']

ANALOGY_TASKS = ['/home/jordan/Documents/Projects/arabic-research/analogy_tasks/questions-words.txt',
                 '/home/jordan/Documents/Projects/arabic-research/analogy_tasks/questions-words-ar.txt']
ANALOGY_OUTPUT_FILES = [RESULTS_DIR+'/en_analogy_results.csv',
                        RESULTS_DIR+'/ar_analogy_results.csv']                    
ANALOGY_OUT_HEADER = ['Embedding File', 'Hit_Percent', 'Scores']

EN_SIM_OUTPUT_FILE = RESULTS_DIR+'/en_similiarity_task_results.csv'

IN_HEADER = ['Word 1', 'Word 2', 'Similarity']
OUT_HEADER = ['Embedding File', 'MSE', 'Accuracy', 'Hit_Percent', 'Correlation', 'Correlation Sig', 'Spearman', 'Spearman Sig']