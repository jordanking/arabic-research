#!/usr/bin/env python
# coding: utf-8

import os
import json

# 5 types to compute: frequency, domain, neighborhood, weighted, and graph [0-4]
BUZZ_TYPE = 0

rootdir = 'text_corpus'
buzzDump = 'file'
groundTruth = 'file'
buzzTimeline = {}
groundTruthTimeline = {}

# list of seed words
domain = []

def main():

    # expand seed words by buzz type
    if BUZZ_TYPE == 3:
        # expand with embeddings
    elif BUZZ_TYPE == 4:
        # build graph

    # compute buzz
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            timestamp, text = parseDocument(os.path.join(subdir, file))
            buzzTimeline[timestamp] += frequencyBuzz(text, domain)

    # save buzz timeline
    with open(buzzDump, 'w') as f:
        json.dump(buzzTimeline, f)

    # load ground truth
    with open(groundTruth, 'r') as f:
        try:
            groundTruthTimeline = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            groundTruthTimeline = {}

    # evaluate buzz

def parseDocument(file):
    document = open(os.path.join(subdir, file), 'rb')
    # parse timestamp
    # extract text
    return timestamp, text

def frequencyBuzz(text, domain):
    buzz = 0
    for word in text.split():

        if BUZZ_TYPE < 3:
            if word in domain:
                buzz += 1
        elif BUZZ_TYPE == 3:
            # weighted
        else:
            # graph?

    return buzz

if __name__ == "__main__":
    main()