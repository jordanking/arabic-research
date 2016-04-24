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

#687840


def main():
    resultsDirectory = '../buzz/results/'
    masterOutput = '../buzz/masterOut.csv'

    domainList = '../buzz/domainlist.txt'
    fullDomain = parseDomainList(domainList)

    buzztype = [0,1,2,3] # freq, dom, neighbors, weighted
    domain = [['عنف','عنيف'],fullDomain,fullDomain,fullDomain]
    corpus = '../buzz/corpus/'
    deathCountFile = '../buzz/iraqDeathCount.csv'
    expansionFactor = 1
    word2vecModel = ['../temp/controldigFalsetashFalsemod1size200wind4.txt', '../temp/tokensdigFalsetashTruemod0size200wind4.txt','../temp/lemmasdigTruetashTruemod1size200wind4.txt']

    # sweep over all of the options, recomputing different types of buzz
    for curr_buzz in buzztype:
        curr_domain = domain[curr_buzz]
        if curr_buzz >= 2:
            for curr_mod in word2vecModel:
                buzzOutputFile = resultsDirectory+'buzz_'+str(curr_buzz)+'_'+curr_mod.split('/')[2]+'.json'
                resultsOutputFile = resultsDirectory+'results_'+str(curr_buzz)+'_'+curr_mod.split('/')[2]+'.csv'

                print('Computing buzz type {} using model {}.'.format(curr_buzz, curr_mod))
                captureBuzz(curr_buzz, curr_domain, corpus, deathCountFile, buzzOutputFile, resultsOutputFile, expansionFactor, curr_mod)
        else:
            buzzOutputFile = resultsDirectory+'buzz_'+str(curr_buzz)+'.json'
            resultsOutputFile = resultsDirectory+'results_'+str(curr_buzz)+'.csv'

            print('Computing buzz type {}.'.format(curr_buzz))
            captureBuzz(curr_buzz, curr_domain, corpus, deathCountFile, buzzOutputFile, resultsOutputFile)

    with open(masterOutput, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['method', 'bs','bp', 'ns', 'np'])

        for outFile in os.listdir(resultsDirectory):
            if outFile.startswith('results'):
                df = pd.read_csv(resultsDirectory+outFile, header='infer')
                method = outFile.split('.')[0]
                bs = df['deaths'].corr(df['buzz'], method='spearman')
                bp = df['deaths'].corr(df['buzz'], method='pearson')
                ns = df['deaths'].corr(df['normalized buzz'], method='spearman')
                np = df['deaths'].corr(df['normalized buzz'], method='pearson')
                print('Method: {} Buzz spear: {} Buzz pear: {} Norm spear: {} Norm pear: {}'.format(method, bs, bp, ns, np))
                csvwriter.writerow([method, bs, bp, ns, np])


def captureBuzz(buzztype, domain, corpus, deathCountFile, buzzFile, resultsFile, expansionFactor=10, word2vecModel=None):
    # expand with embeddings
    query = {}

    # for all types, seed words have weight of 1
    for word in domain:
        word = word.strip().decode('UTF-8', 'replace')
        query[word] = 1.0

    # for types 2 and 3, add expansionFactor words to query for each word in query
    if buzztype >= 2:

        # collect new words with word2vec
        newWords = {}

        # load model
        print('Loading word2vec model...')
        model = Word2Vec.load_word2vec_format(word2vecModel.strip(), binary=True)
        
        print('Expanding query...')
        for word in query:
            try:
                for weighted in expandQuery(word, model, expansionFactor):
                    if weighted[0] not in newWords:
                        newWords[weighted[0]] = [weighted[1]]
                    else:
                        newWords[weighted[0]].append(weighted[1])
            except Exception:
                continue

        # average the weights of the new words for the expansion
        for word in newWords:
            if word not in query:
                query[newWords[word]] = sum(newWords[word])/float(len(newWords[word]))

    # if type is 2, we don't care about similarity weights, everything is 1
    if buzztype == 2:
        for key in query:
            query[key] = 1.0

    # print('Query: {}'.format(query))

    # compute buzz
    buzzTimeline = {}
    fileCounter = 0

    for subdir, dirs, files in os.walk(corpus):
        for file in files:
            fileCounter += 1
            sys.stdout.write('\rProcessing file: {}...'.format(fileCounter))
            sys.stdout.flush()

            try:
                timestamp, docId, text = parseDocument(os.path.join(subdir, file))
            except Exception:
                continue

            monthstamp = str(timestamp.year) + '-' + str(timestamp.month)

            buzz, wordCount = domainBuzz(text, query)

            if timestamp in buzzTimeline:
                buzzTimeline[monthstamp][0] += wordCount
                buzzTimeline[monthstamp][1] += buzz
            else:
                buzzTimeline[monthstamp] = [wordCount,buzz]

    # save buzz timeline
    with open(buzzFile, 'w') as f:
        json.dump(buzzTimeline, f, sort_keys=True, indent=4, separators=(',', ': '))
    print('\nBuzz saved to: {}'.format(buzzFile))

    # load ground truth
    deathCountTimeline = loadDeathCount(deathCountFile)

    # print(buzzTimeline)
    # print(deathCountTimeline)

    # evaluate buzz
    with open(resultsFile, 'wb') as csvfile:
        buzzwriter = csv.writer(csvfile, delimiter=',')
        buzzwriter.writerow(['period', 'deaths','word count', 'buzz', 'normalized buzz'])

        for period in deathCountTimeline:
            if period in buzzTimeline:
                # print('Period: {}, deaths: {}, buzz: {}'.format(period, deathCountTimeline[period], buzzTimeline[period][1]))
                buzzwriter.writerow([period, deathCountTimeline[period], buzzTimeline[period][0], buzzTimeline[period][1], buzzTimeline[period][1]/buzzTimeline[period][0]])
            else:
                pass
                # print('Period: {} was not found in the buzz timeline.'.format(period))
    print('Results saved to: {}\n'.format(resultsFile))

def parseDocument(file):
    tree = ET.parse(file)
    root = tree.getroot()

    docId = root.find('Id').text
    docDate = datetime.datetime.strptime(root.find('PublicationDateTime').text, '%d %b %Y %H:%M:%S')
    # docDate = docDate.strftime("%d %b %Y %H:%M:%S")
    docText = root.find('Text').text

    return [docDate, docId, docText]

def loadDeathCount(deathCountFile):

    df = pd.read_csv(deathCountFile, header='infer', skiprows=10)
    deathCountTimeline = {}

    for i, row in df.iterrows():
        if not pd.isnull(row['dataset 1']):
            datestamp = datetime.datetime.strptime('01 ' + row['Month starting'][2:], '%d %b %Y')
            monthstamp = str(datestamp.year) + '-' + str(datestamp.month)
            deathCountTimeline[monthstamp] = row['dataset 1']

    # deathCountTimeline = IntervalTree()
    # for i, row in df.iterrows():
    #     if not pd.isnull(row['dataset 1']):
    #         datestamp = datetime.datetime.strptime('01 ' + row['Month starting'][2:], '%d %b %Y')
    #         timestamp = time.mktime(datestamp.timetuple())
    #         timestamp = int(timestamp)
    #         print('Time: {}, Value: {}'.format(timestamp, row['dataset 1']))
    #         deathCountTimeline[timestamp:timestamp] = row['dataset 1']

    return deathCountTimeline

def domainBuzz(text, query):
    buzz = 0.0
    wordCount = 0
    for word in text.split():
        wordCount += 1
        if word in query:
            buzz += query[word]
        else:
            pass
            # print('Word: {} not found in'.format(word.encode('UTF-8', 'replace')))
            # print('query: {}.'.format(query.keys()))
    return [buzz, wordCount]

def parseDomainList(file):
    domainList = []
    with open(file, 'rb') as data:
        for line in data:
            if line not in domainList:
                domainList.append(line)

    return domainList


def expandQuery(query, model, target_n):
    """ Takes a query word, returns n words with similarity weights from the word2vec model """
    while True:
        # query = query.decode('UTF-8', 'replace')
        similar_words = None

        try:
            similar_words = model.most_similar(word, topn=(target_n-1))
        except KeyError as ke:
            print("Query couldn't be expanded.")

        new_query = similar_words.append((query, 1.0))

        # for word in new_query:
        #     word.encode('UTF-8','replace')

        return new_query

if __name__ == "__main__":
    main()