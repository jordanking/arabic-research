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
import pandas as pd



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

OUTPUT_FILE = 'similarity_task_merged.csv'
OUTPUT_FILE_2 = 'similarity_task_multi_vote.csv'
OUTPUT_FILE_3 = 'similarity_task_4_votes.csv'


IN_HEADER = ['Word 1', 'Word 2', 'Similarity (0-5)', 'Nonsense (Optional)']
SIMILARITY_OPT = 'Similarity (0-10)'
OUT_HEADER = ['Word 1', 'Word 2', 'Similarity']

try:
    os.remove(OUTPUT_FILE)
except OSError as e:
    print('Output file did not exist')

try:
    os.remove(OUTPUT_FILE_2)
except OSError as e:
    print('Output file did not exist')

try:
    os.remove(OUTPUT_FILE_3)
except OSError as e:
    print('Output file did not exist')

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

twos = np.empty((0,2))
threes = np.empty((0,3)) 
fours = np.empty((0,4))

i = 0
for key in pairs:
    
    votes[i] = len(pairs[key]['value'])
    means[i] = np.mean(pairs[key]['value'])

    if votes[i] == 2:
        twos = np.vstack((twos, pairs[key]['value']))
    elif votes[i] == 3:
        threes = np.vstack((threes, pairs[key]['value']))
    elif votes[i] == 4:
        fours = np.vstack((fours, pairs[key]['value']))

    pairs[key]['flagged'] = False if len(pairs[key]['junk']) == 0 else True
    pairs[key]['votes'] = votes[i]
    pairs[key]['mean'] = means[i]
    
    i += 1

print(describe(means))
print(describe(votes))


twos = pd.DataFrame(data=twos,    # values
             index=twos[:,0],    # 1st column as index
             columns=[0,1])  # 1st row as the column name
print('twos')
print(twos.corr())

threes = pd.DataFrame(data=threes,    # values
             index=threes[:,0],    # 1st column as index
             columns=[0,1,2])  # 1st row as the column name
print('threes')
print(threes.corr())

fours = pd.DataFrame(data=fours,    # values
             index=fours[:,0],    # 1st column as index
             columns=[0,1,2,3])  # 1st row as the column name
print('fours')
print(fours.corr())

plt.hist(means)
plt.hist(votes, color = 'r', alpha = 0.5)
# plt.show()



count = 0
with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for key in pairs:
        if not pairs[key]['flagged']:
            count += 1
            writer.writerow([key[0], key[1], round(pairs[key]['mean'], 3)])

print('Wrote %d word pairs to file %s.' % (count, OUTPUT_FILE))


count = 0
with open(OUTPUT_FILE_2, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for key in pairs:
        if pairs[key]['votes'] < 2:
            continue
        if not pairs[key]['flagged']:
            count += 1
            writer.writerow([key[0], key[1], round(pairs[key]['mean'], 3)])

print('Wrote %d word pairs to file %s.' % (count, OUTPUT_FILE_2))

count = 0
with open(OUTPUT_FILE_3, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(OUT_HEADER)
    for key in pairs:
        if pairs[key]['votes'] < 4:
            continue
        if not pairs[key]['flagged']:
            count += 1
            writer.writerow([key[0], key[1], round(pairs[key]['mean'], 3)])

print('Wrote %d word pairs to file %s.' % (count, OUTPUT_FILE_3))

twos.corr().to_csv('two_corr.csv', sep=',')
threes.corr().to_csv('three_corr.csv', sep=',')
fours.corr().to_csv('four_corr.csv', sep=',')