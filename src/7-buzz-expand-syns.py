#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import os
import csv
import sys
import json
import xml.etree.ElementTree as ET
import datetime
import time
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

sys.path.insert(0,"/Users/jordanking/Documents/")
import arapy.thesaurus as thes

def main():

    domainOut = '../buzz/syn_domainlist.csv'
    domainList = '../buzz/domainlist.txt'
    fullDomain = parseDomainList(domainList)
    startSize = len(fullDomain)

    expansionFactor = 5
    newWords = []

    print('Expanding query...')
    for word in fullDomain:
        try:
            candidates = expandQuerySynonyms(word, expansionFactor)['syn']
            for synonym in candidates:
                if synonym not in newWords:
                    newWords.append(synonym)
        except Exception as e:
            print(e)
            continue
        print("Now at {} new words.".format(len(newWords)))

    for word in newWords:
        if word not in fullDomain:
            fullDomain.append(word)

    endSize = len(fullDomain)

    print("Expanded {} words to {} words with the thesaurus.".format(startSize, endSize))
    print(fullDomain)
    # sweep over all of the options, recomputing different types of buzz    
    with open(domainOut, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for word in fullDomain:
            print(word)
            csvwriter.writerow(word.decode('utf-8'))


def parseDomainList(file):
    domainList = []
    with open(file, 'rb') as data:
        for line in data:
            if line not in domainList:
                domainList.append(line)
    return domainList

def expandQuerySynonyms(query, target_n):
    """ Takes a query word, returns n words with similarity weights from thesaurus """
    # query = query.decode('UTF-8', 'replace')
    similar_words = None
    try:
        similar_words = thes.thesaurus(query, 'syn', ngram=1, ar=True, target_result_count=target_n)
    except KeyError as ke:
        print("Syn lookup failed.")
    return similar_words

if __name__ == "__main__":
    main()