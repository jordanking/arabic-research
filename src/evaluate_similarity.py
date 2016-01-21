# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
import csv
import logging
import os
import numpy as np
from gensim.models import Word2Vec
from scipy.stats.stats import pearsonr  



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

TASK_FILE = '/home/jordan/Documents/Projects/arabic-research/pairs/similarity_task_merged.csv'
TASK_FILE = '/home/jordan/Documents/Projects/arabic-research/CLSR-EK/WS353_ar.csv'
OUTPUT_FILE = 'similiarity_task_results.csv'
IN_HEADER = ['Word 1', 'Word 2', 'Similarity']
OUT_HEADER = ['Embedding File', 'Accuracy']

embeddings = ['/media/jordan/Media/data/arabic/arwiki-20150901-pages-articles_parsed_ar_onlyTrue_digitsTrue_alifTrue_hamzaTrue_yaaTrue_tashkilTrue_sg0_size100_window8_min_count5_sample0.0001_hs0_negative25_iter15.bin']

# load task
pairs = {}
with open(TASK_FILE, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:   
        key = (row[IN_HEADER[0]], row[IN_HEADER[1]])

        value = float(row[IN_HEADER[2]])

        pairs[key] = {'value':value, 
                      'scores':np.zeros(len(embeddings)), 
                      'diffs':np.zeros(len(embeddings))}

# run task
means = np.zeros(len(embeddings))
for m in range(len(embeddings)):

    modelfile = embeddings[m]
    model = Word2Vec.load_word2vec_format(modelfile, binary=True)

    total_diff = 0
    hits = 0
    misses = 0


    print("Evaluating " + str(len(pairs)) + " pairs")
    
    scores = []
    values = []

    for key in pairs:

        try:
           
            # print(model[key[0].decode('UTF-8', 'replace')])
            # print(np.dot(model[key[0].decode('UTF-8', 'replace')], model[key[1].decode('UTF-8', 'replace')]))
            # print(model.similarity(key[0].decode('UTF-8', 'replace'),
                                   # key[1].decode('UTF-8', 'replace')))
            pairs[key]['scores'][m] = abs(model.similarity(key[0].decode('UTF-8', 'replace'),
                                                       key[1].decode('UTF-8', 'replace')))
            pairs[key]['diffs'][m] = abs(pairs[key]['scores'][m] - pairs[key]['value'])

            # print(str(pairs[key]['scores'][m]) + " vs " + str(pairs[key]['value']))
            
            scores.append(pairs[key]['scores'][m])
            values.append(pairs[key]['value'])
            print(str(scores[-1]) + " " + str(values[-1]))
            
            total_diff += pairs[key]['diffs'][m]
            hits += 1
        except KeyError as ke:
            #print(str(misses) + ke.message.encode('utf-8','replace'))
            misses += 1
            continue

    
    print(pearsonr(scores, values))    
    print("Hits: " + str(hits))
    print("Misses: " + str(misses))
    means[m] = total_diff / max(hits, 1)

# save results
with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for m in range(len(embeddings)):
        writer.writerow([embeddings[m], means[m]])