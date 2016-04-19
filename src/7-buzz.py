#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import json
import datetime
import intervaltree


# 4 types to compute: frequency, domain, neighborhood, and weighted
BUZZ_TYPE = 0

rootdir = 'text_corpus'
buzzDump = 'file'
groundTruth = 'file'
deathCountFile = 'some.csv'
buzzTimeline = IntervalTree()

firstDay = #?
lastDay = #?

# list of seed words
domain = []

def main():

    # expand with embeddings
    if BUZZ_TYPE == 3:
        pass # TODO

    # TODO add weights to domain?

    # compute buzz
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            timestamp, text = parseDocument(os.path.join(subdir, file))
            buzzTimeline[timestamp] += domainBuzz(text, domain)

    # save buzz timeline
    with open(buzzDump, 'w') as f:
        json.dump(buzzTimeline, f)

    # load ground truth
    deathCountTimeline = loadDeathCount(deathCountFile)

    # evaluate buzz
    # query each interval in gt
    # sum buzz in that interval as result
    # compare gt interval value to result

def parseDocument(file):
    document = open(os.path.join(subdir, file), 'rb')
    
    # parse timestamp
    # convert to seconds

    # extract text

    return timestamp, text

def loadDeathCount(deathCountFile):

    df = pd.read_csv(deathCountFile, header=True, skiprows=10)

    deathCountTimeline = IntervalTree()

    for i, row in df.iterrows():
        timestamp = datetime.strptime('01 ' + row['Month Starting'][2:], '%d %b %Y')
        deathCountTimeline[timestamp:timestamp] = row['dataset 1']

def domainBuzz(text, domain):
    # parameter to weight all words?

    buzz = 0
    for word in text.split():

        if BUZZ_TYPE < 3:
            if word in domain:
                buzz += 1
        else:
            # weighted

    return buzz

if __name__ == "__main__":
    main()