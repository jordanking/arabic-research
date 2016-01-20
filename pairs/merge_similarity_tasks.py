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

OUTPUT_FILE = 'similiarity_task_merged.csv'
IN_HEADER = ['Word 1', 'Word 2', 'Similarity (0-5)', 'Nonsense (Optional)']
SIMILARITY_OPT = 'Similarity (0-10)'
OUT_HEADER = ['Word 1', 'Word 2', 'Similarity']

os.remove(OUTPUT_FILE)
pairs = {}

for filename in os.listdir(os.getcwd()):
    if(filename[-4:] == '.csv'):
        with open(filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                # one file was completed on a 0-10 scale
                scale_key = IN_HEADER[2]
                if SIMILARITY_OPT in row:
                    scale_key = SIMILARITY_OPT

                try:
                    key = (row[IN_HEADER[0]], row[IN_HEADER[1]])

                    value = float(row[scale_key])
                    if scale_key == SIMILARITY_OPT:
                        value = value / 10.0
                    else:
                        value = value / 5.0

                    if key not in pairs:
                        pairs[key] = {'value':[], 'junk':[]}

                    pairs[key]['value'].append(value)

                    # if the pair was flagged as nonsense, note it
                    if row[IN_HEADER[3]]:
                        pairs[key]['junk'].append(row[IN_HEADER[3]])
                    

                except ValueError as ex:
                    # the cell wasn't filled / wasn't correctly filled
                    pass

means = np.zeros(len(pairs))

votes = np.zeros(len(pairs))
i = 0
for key in pairs:
    votes[i] = len(pairs[key]['value'])
    means[i] = np.mean(pairs[key]['value'])

    pairs[key]['flagged'] = False if len(pairs[key]['junk']) == 0 else True
    pairs[key]['votes'] = votes[i]
    pairs[key]['mean'] = means[i]
    
    i += 1

print(describe(means))
print(describe(votes))

plt.hist(means)
plt.hist(votes, color = 'r', alpha = 0.5)
plt.show()

with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for key in pairs:
        if not pairs[key]['flagged']:
            writer.writerow([key[0], key[1], round(pairs[key]['mean'], 3)])