# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
import csv
import logging
import os
import numpy as np
from scipy.stats import describe
import matplotlib.pyplot as plt
import plotly.plotly as py



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

INPUT_FILE = 'WS353.csv'
OUTPUT_FILE = 'WS353_ar.csv'
EN_OUTPUT_FILE = 'WS353_en.csv'
IN_HEADER = ["EN.1","EN.2","RO.1","RO.2","AR.1","AR.2","ES.1","ES.2","score"]
OUT_HEADER = ['Word 1', 'Word 2', 'Similarity']

# os.remove(OUTPUT_FILE)
pairs = {}
en_pairs = {}

with open(INPUT_FILE, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ';',quotechar='"')
    for row in reader:

        try:
            key = (row[IN_HEADER[4]], row[IN_HEADER[5]])
            en_key = (row[IN_HEADER[0]], row[IN_HEADER[1]])

            value = float(row[IN_HEADER[8]])
            
            value = value / 10.0

            pairs[key] = value
            en_pairs[en_key] = value

        except ValueError as ex:
            # the cell wasn't filled / wasn't correctly filled
            pass

means = np.zeros(len(pairs))

i = 0
for key in pairs:
    
    means[i] = pairs[key]
    i += 1

print(describe(means))
plt.hist(means)
plt.show()

with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for key in pairs:
        writer.writerow([key[0], key[1], round(pairs[key], 3)])

with open(EN_OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for key in en_pairs:
        writer.writerow([key[0], key[1], round(en_pairs[key], 3)])