# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
import csv
import logging
import sys
import os
ARAPY_PATH = "/home/jordan/Documents/Projects/"
sys.path.insert(0,ARAPY_PATH)
from arapy.translate import translate_list

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

INPUT_FILE = 'questions-words.txt'
OUTPUT_FILE = 'questions-words-ar.txt'

analogies = []
with open(INPUT_FILE, 'rb') as csvfile:
    reader = csv.DictReader(filter(lambda row: row[0]!=':', csvfile), fieldnames=['a', 'b', 'c', 'd'], delimiter = ' ')
    for row in reader:
        analogies.append([row['a'], row['b'], row['c'], row['d']])

ar_analogies = []
for analogy in analogies:
    ar_analogy = []
    for word in analogy:
        ar_analogy.append(translate_list([word], 'ar'))
    ar_analogies.append(ar_analogy)

with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for analogy in ar_analogies:
        writer.writerow(analogy)
