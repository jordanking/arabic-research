#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
from constants import ARAPY_PATH, WORKING_DIRECTORY, EMBEDDING_DIR, RESULTS_DIR
from constants import ANALOGY_TASKS, ANALOGY_OUTPUT_FILES, ANALOGY_OUT_HEADER
import logging
import csv
import logging
import os
import numpy as np
from gensim.models import Word2Vec
from gensim import matutils

import StringIO
import sys
sys.path.insert(0,ARAPY_PATH)
from arapy.madamira import Madamira
from arapy.normalization import normalize

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

ARABIC = True
TASK_FILE = ANALOGY_TASKS[1]
# TASK_FILE = '/home/jordan/Documents/Projects/arabic-research/analogy_tasks/test_ar.txt'
ACC_OUT = ANALOGY_OUTPUT_FILES[1]

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


def analogyTest(key1, key2, key3, key4, model, params, mada):

    key1 = key1.split(' ')
    key2 = key2.split(' ')
    key3 = key3.split(' ')
    key4 = key4.split(' ')

    pos = [part.decode('utf-8', 'replace') for part in (key2 + key3)]
    neg = [part.decode('utf-8', 'replace') for part in key1]
    sims = model.most_similar(positive=pos, negative=neg, topn=False)
    
    for index in matutils.argsort(sims, reverse=True):

        word = model.index2word[index].encode('utf-8')
        
        if word not in set(key1+key2+key3):
            # print("Accepted result: %s and %s" % (word, key4))
            if word not in key4:
                return 0
            else:
                return 1
    
embeddings = None
if ARABIC:
    embeddings = os.listdir(EMBEDDING_DIR)
else:
    embeddings = ['/media/jordan/Media/data/word2vec/GoogleNews-vectors-negative300.bin',
                  '/home/jordan/Desktop/english_5mil.bin',
                  '/home/jordan/Desktop/english_9mil.bin',
                  '/home/jordan/Desktop/english_20mil.bin']#,

# load base task
analogies = []
delim = ' '
if ARABIC:
    delim = ','
with open(TASK_FILE, 'rb') as csvfile:
    reader = csv.DictReader(filter(lambda row: row[0]!=':', csvfile), 
                            fieldnames=['a', 'b', 'c', 'd'], 
                            delimiter = delim)
    for row in reader:
        # print(row)
        analogies.append([row['a'], row['b'], row['c'], row['d']])

# run  tasks
scores = np.zeros(len(embeddings))
hit_percents = np.zeros(len(embeddings))
task_size = len(analogies)

with Madamira() as mada:
    for m in range(len(embeddings)):
        modelfile = embeddings[m]

        params = None
        if ARABIC:
            params = parseParameters(modelfile)
            modelfile = EMBEDDING_DIR + '/' + modelfile

        # load word2vec model
        model = Word2Vec.load_word2vec_format(modelfile, binary=True)

        score = 0
        hits = 0

        for analogy in analogies:
            try:
                print('\n')
                
                key1 = analogy[0]
                key2 = analogy[1]
                key3 = analogy[2]
                key4 = analogy[3]

                if ARABIC:
                    key1 = preprocessKey(analogy[0], params, mada)
                    key2 = preprocessKey(analogy[1], params, mada)
                    key3 = preprocessKey(analogy[2], params, mada)
                    key4 = preprocessKey(analogy[3], params, mada)

                # print('Processed Analogy: %s %s %s %s' % (key1, key2, key3, key4))

                result = analogyTest(key1, key2, key3, key4, model, params, mada)

                print("result: %d" % (result))
                
                score += result
                hits += 1

            except KeyError as ke:
                logging.info("Miss.")
                continue

        
        print("Score: %f" % (score*1.0/max(1, hits)))

        scores[m] = score*1.0/max(hits, 1)
        hit_percents[m] = hits / task_size


# save results
with open(ACC_OUT, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(ANALOGY_OUT_HEADER)

    for m in range(len(embeddings)):
        writer.writerow([embeddings[m], hit_percents[m], scores[m]])
