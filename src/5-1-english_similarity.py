#!/usr/bin/env python
# coding: utf-8

# ARAPY_PATH = "/home/jordan/Documents/Projects/"
# WORKING_DIRECTORY = "/home/jordan/Documents/Projects/arabic-research/temp"
# EMBEDDINGS_DIR = WORKING_DIRECTORY+"/4-embeddings"
# RESULTS_DIR = WORKING_DIRECTORY+"/5-semantic_results"
# TASKS = ['/home/jordan/Documents/Projects/arabic-research/pairs/similarity_task_merged.csv',
#          '/home/jordan/Documents/Projects/arabic-research/CLSR-EK/WS353_ar.csv']
# TASK_FILE = TASKS[0]
# OUTPUT_FILE = RESULTS_DIR+'/similiarity_task_results.csv'
# IN_HEADER = ['Word 1', 'Word 2', 'Similarity']
# OUT_HEADER = ['Embedding File', 'Accuracy']

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
from constants import ARAPY_PATH, WORKING_DIRECTORY, EMBEDDING_DIR, RESULTS_DIR
from constants import TASKS, EN_SIM_OUTPUT_FILE, IN_HEADER, OUT_HEADER
import logging
import csv
import logging
import os
import numpy as np
from gensim.models import Word2Vec
from scipy.stats.stats import pearsonr  
import scipy.stats.spearmanr
import sys
sys.path.insert(0,ARAPY_PATH)
from arapy.madamira import Madamira

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

#### obtain the various embeddings that need evaluation
#### english baselines (absolute paths)
# EN_SIM_OUTPUT_FILE = '/home/jordan/Desktop/english_eval.txt'

english_embeddings = ['/media/jordan/Media/data/word2vec/GoogleNews-vectors-negative300.bin',
                      '/home/jordan/Desktop/english_5mil.bin',
                      '/home/jordan/Desktop/english_9mil.bin',
                      '/home/jordan/Desktop/english_20mil.bin']#,
                      # '/home/jordan/Desktop/english_100mil.bin']
# english_embeddings = ['/home/jordan/Desktop/english_5mil2.bin']
english_task = TASKS[2]
EN_SIM_OUTPUT_FILE = '/home/jordan/Desktop/itworks.csv'

# load a single task
e_pairs = {}
with open(english_task, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:   
        key = (row[IN_HEADER[0]], row[IN_HEADER[1]])

        value = float(row[IN_HEADER[2]])

        e_pairs[key] = {'value':value, 
                      'scores':np.zeros(len(english_embeddings)),
                      'se':np.zeros(len(english_embeddings)), 
                      'diffs':np.zeros(len(english_embeddings))}

# run english task
e_means = np.zeros(len(english_embeddings))
e_mse = np.zeros(len(english_embeddings))
e_hit_percents = np.zeros(len(english_embeddings))
e_correlations = np.zeros(len(english_embeddings))
e_correlations_sig = np.zeros(len(english_embeddings))
e_spearmans = np.zeros(len(english_embeddings))
e_spearmans_sig = np.zeros(len(english_embeddings))


for m in range(len(english_embeddings)):

    # identify parameters from training
    modelfile = english_embeddings[m]

    # load word2vec model
    model = Word2Vec.load_word2vec_format(modelfile, binary=True)

    total_diff = 0
    total_se = 0
    hits = 0
    misses = 0
    scores = []
    values = []

    for key in e_pairs:
        try:
            # TODO score the processed keys
            # TODO get the scores via combination of token vecs, etc
            # logging.info("keys: " + key[0] + ' ' + key[1])
            keyscore = abs(model.similarity(key[0],key[1]))
            # logging.info("Keyscore: " + str(keyscore))
            e_pairs[key]['scores'][m] = keyscore

            # get the difference between the task estimate and model estimate
            e_pairs[key]['diffs'][m] = abs(keyscore - e_pairs[key]['value'])

            e_pairs[key]['se'][m] = pow(keyscore - e_pairs[key]['value'], 2)
            
            scores.append(keyscore)
            values.append(e_pairs[key]['value'])

            # logging.info("guess: " + str(scores[-1]))
            # logging.info("actual: " + str(values[-1]))
            
            total_diff += e_pairs[key]['diffs'][m]
            total_se += e_pairs[key]['se'][m]


            hits += 1

        except KeyError as ke:
            #print(str(misses) + ke.message.encode('utf-8','replace'))
            logging.info('Missed a pair.')
            misses += 1
            continue

    correlation = pearsonr(scores, values)
    e_correlations[m] = correlation[0]
    e_correlations_sig[m] = correlation[1]

    spearman = spearmanr(scores, values)
    e_spearmans[m] = spearman[0]
    e_spearmans_sig[m] = spearman[1]

    logging.info("Score-value correlation: " + str(e_correlations[m]))
    logging.info("Spearman: " + str(e_spearmans[m]))
    logging.info("Pairs evaluated: " + str(hits))
    logging.info("Pairs not found: " + str(misses))

    e_means[m] = total_diff / max(hits, 1)
    e_mse[m] = total_se / max(hits, 1)
    e_hit_percents[m] = hits / max(1, (hits+misses))

# save results
with open(EN_SIM_OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)

    for m in range(len(english_embeddings)):
        writer.writerow([english_embeddings[m], e_mse[m], e_means[m], e_hit_percents[m], e_correlations[m], e_correlations_sig[m], e_spearmans[m], e_spearmans_sig[m]])

