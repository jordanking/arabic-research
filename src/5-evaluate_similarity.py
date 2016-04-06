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
from constants import TASKS, AR_SIM_OUTPUT_FILE, AR_SIM_OUTPUT_FILE_2, IN_HEADER, OUT_HEADER
import logging
import csv
import logging
import os
import numpy as np
from gensim.models import Word2Vec
from scipy.stats.stats import pearsonr
import scipy.stats.spearmanr
import StringIO
import sys
sys.path.insert(0,ARAPY_PATH)
from arapy.madamira import Madamira
from arapy.normalization import normalize

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

TASK_FILE = TASKS[1]
SIM_OUT = AR_SIM_OUTPUT_FILE_2
# SIM_OUT = '/home/jordan/Documents/Projects/arabic-research/writeup/acl2016/results/preprocessing_eval_1.csv'

def parseParameters(filename):
    #controldigTruetashTruemod1size200wind7.txt
    params = {}
    logging.info(filename)
    preprocessing_options = ['control', 'lemmas', 'tokens']
    for opt in preprocessing_options:
        if filename.startswith(opt):
            params['preprocessing'] = opt
            filename = filename[len(opt):]

    logging.info(filename)
    normalization_options = ['dig', 'tash']
    for opt in normalization_options:
        filename = filename[len(opt):]
        if filename.startswith('True'):
            params[opt] = True
            filename = filename[4:]
        else:
            params[opt] = False
            filename = filename[5:]

    model_options = ['mod', 'size', 'wind']
    logging.info(filename)
    for opt in model_options:
        filename = filename[len(opt):]
        value = ''
        for char in filename:
            if char.isdigit():
                value += char
            else:
                break
        params[opt] = int(value)
        filename = filename[len(value):]

    return params

def preprocessKey(inkey, params, mada):
    key = inkey

    if params['preprocessing'] == 'lemmas':
        out = mada.process([key])
        buff = StringIO.StringIO()
        for doc in out.docs():
            for sent in doc.sentences():
                for word in sent.words():
                    buff.write(word.lemma())
                    buff.write(" ")
        buff.seek(0)
        key = buff.read().rstrip()#.encode('utf8')

    elif params['preprocessing'] == 'tokens':
        out = mada.process([key])
        buff = StringIO.StringIO()
        for doc in out.docs():
            for sent in doc.sentences():
                for word in sent.words():
                    for token in word.tokens():
                        buff.write(token)
                        buff.write(" ")
        buff.seek(0)
        key = buff.read().rstrip()#.encode('utf8')
  
    if params['preprocessing'] == 'control':
        key = key.decode('utf8')

    key = normalize(key, ar_only=True, digits=params['dig'], 
                    alif=True, hamza=True, yaa=True, tashkil=params['tash'])

    return key.encode('utf8')


def get_similarity(key1, key2):
    keyset1 = set(key1.decode('UTF-8', 'replace').split(' '))
    keyset2 = set(key2.decode('UTF-8', 'replace').split(' '))
    return abs(model.n_similarity(keyset1,keyset2))


#### obtain the various embeddings that need evaluation
#### arabic embeddings
embeddings = os.listdir(EMBEDDING_DIR)

# embeddings = os.listdir('/home/jordan/Desktop/vecs/')
# EMBEDDING_DIR = '/home/jordan/Desktop/vecs'

# load base task
pairs = {}
with open(TASK_FILE, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:   
        key = (row[IN_HEADER[0]], row[IN_HEADER[1]])

        value = float(row[IN_HEADER[2]])

        pairs[key] = {'value':value, 
                      'scores':np.zeros(len(embeddings)),
                      'se':np.zeros(len(embeddings)),
                      'diffs':np.zeros(len(embeddings))}

# run arabic tasks
means = np.zeros(len(embeddings))
mse = np.zeros(len(embeddings))
hit_percents = np.zeros(len(embeddings))
correlations = np.zeros(len(embeddings))
correlations_sig = np.zeros(len(embeddings))
spearmans = np.zeros(len(embeddings))
spearmans_sig = np.zeros(len(embeddings))


with Madamira() as mada:
    for m in range(len(embeddings)):
        # identify parameters from training
        modelfile = embeddings[m]
        params = parseParameters(modelfile)

        # load word2vec model
        model = Word2Vec.load_word2vec_format(EMBEDDING_DIR + '/' + modelfile, binary=True)

        total_diff = 0
        total_se = 0
        hits = 0
        misses = 0
        scores = []
        values = []

        for key in pairs:
            try:
                print('\n')
                # logging.info("pre-Key1: " + str(key[0]))
                # logging.info("pre-Key2: " + str(key[1]))
                
                # TODO preprocess the keys with the parameters
                key1 = preprocessKey(key[0], params, mada)
                key2 = preprocessKey(key[1], params, mada)

                # TODO score the processed keys
                logging.info("Key1: " + str(key1))
                logging.info("Key2: " + str(key2))

                keyscore = abs(get_similarity(key1, key2))
                pairs[key]['scores'][m] = keyscore

                # get the difference between the task estimate and model estimate
                pairs[key]['diffs'][m] = abs(keyscore - pairs[key]['value'])
                pairs[key]['se'][m] = pow(keyscore - pairs[key]['value'], 2)
                
                scores.append(keyscore)
                values.append(pairs[key]['value'])

                print("guess: " + str(scores[-1]))
                print("actual: " + str(values[-1]))
                
                total_diff += pairs[key]['diffs'][m]
                total_se += pairs[key]['se'][m]

                hits += 1

            except KeyError as ke:
                #print(str(misses) + ke.message.encode('utf-8','replace'))
                logging.info("Miss.")
                misses += 1
                continue

        correlation = pearsonr(scores, values)
        correlations[m] = correlation[0]
        correlations_sig[m] = correlation[1]

        spearman = spearmanr(scores, values)
        spearmans[m] = spearman[0]
        spearmans_sig[m] = spearman[1]


        print("Score-value correlation: " + str(correlation))
        print("Spearman: " + str(spearman))
        print("Pairs evaluated: " + str(hits))
        print("Pairs not found: " + str(misses))

        means[m] = total_diff / max(hits, 1)
        mse[m] = total_se / max(hits, 1)
        hit_percents[m] = hits / max(1, (hits+misses))


# save results
with open(SIM_OUT, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)

    for m in range(len(embeddings)):
        writer.writerow([embeddings[m], mse[m], means[m], hit_percents[m], correlations[m], correlations_sig[m], spearmans[m], spearmans_sig[m]])
