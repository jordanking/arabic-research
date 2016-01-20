# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
import csv
import logging
import os
import numpy as np


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

TASK_FILE = 'similarity_task_merged.csv'
OUTPUT_FILE = 'similiarity_task_results.csv'
IN_HEADER = ['Word 1', 'Word 2', 'Similarity']
OUT_HEADER = ['Embedding File', 'Accuracy']

embeddings = ['file1', 'file2']

# load task
pairs = {}
with open(TASK_FILE, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:   
        key = (row[IN_HEADER[0]], row[IN_HEADER[1]])

        value = float(row[scale_key])

        pairs[key] = {'value':value, 
                      'scores':np.zeros(len(embeddings)), 
                      'diffs':np.zeros(len(embeddings))}

# run task
means = np.array()
for m in range(len(embeddings)):
    total_diff = 0
    for key in pairs:
        pairs[key]['scores'][m] = embeddings[m].similarity(key[0],key[1])
        pairs[key]['differences'][m] = abs(pairs[key]['scores'][m] - pairs[key]['value'])
        total_diff += pairs[key]['differences'][m]
    means[m] = total_diff / len(pairs)

# save results
with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for m in range(len(embeddings)):
        writer.writerow([embeddings[m], means[m]])