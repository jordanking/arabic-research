#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import gensim
import logging
import sys
import random

sys.path.insert(0,"/Users/jordanking/Documents/")
import arapy.thesaurus as thes
import arapy.normalization as norm
import arapy.madamira as mada

# random seeding for reproducing
random.seed(1)

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# file to extract most common from
sourcefile = "/Users/jordanking/Documents/data/arwiki/arwiki-20150901-pages-articles_parsed.txt"
# sourcefile = "/Users/jordanking/Documents/data/arwiki/arwiki4k.txt"

# task file prefix
taskfile_prefix = "similarity_task_"

# percent of sentences a word must be in to be ignored as a stop word
stopword_thresh = 0.05

# number of task files
task_count = 5
task_size = 250
synonym_percent = 0.5
antonym_percent = 0.25
shuffle_percent = 0.25

synonym_target = task_size*task_count*(synonym_percent+shuffle_percent)
antonym_target = task_size*task_count*(antonym_percent+shuffle_percent)
top_n = int((synonym_target + antonym_target)*8)

logging.info("Top word count is: " + str(top_n))

synonym_count = 0
antonym_count = 0

# get most common words that don't appear in more than five percent of the sentences
logging.info("Building dictionary of top words")
document = gensim.corpora.dictionary.Dictionary()
with open(sourcefile, 'r') as doc_file:
    for line in doc_file:
        document.doc2bow(line.split(), allow_update=True)
document.filter_extremes(no_below=5, no_above=stopword_thresh, keep_n=top_n)
word_list = document.values()

# # word_list = most_common_words(text_source, top_n, skip_stop_words)
current_word = 0

synonym_pairs = []
antonym_pairs = []

# build word lists
with mada.Madamira() as madamira:
    while current_word < top_n:

        query = norm.normalize(word_list[current_word], ar_only=True, digits=True, alif=False, hamza=False, yaa=False, tashkil=False).strip('#')

        if len(query) > 0:

            if synonym_count < synonym_target:
                lookups = thes.thesaurus(query.encode('utf-8'), 'syn', ngram=1, ar=True, target_result_count=1)
                if 'syn' in lookups:
                    if len(lookups['syn']) > 0:
                        candidate = norm.normalize(lookups['syn'][0], ar_only=True, digits=True, alif=False, hamza=False, yaa=False, tashkil=False).strip('#').strip()
                        if len(candidate) > 1:

                            # make sure the normalized and lemma forms are not the same
                            
                            query_lemma = madamira.process_sentence(query.encode('utf-8'))[0].lemma()
                            candidate_lemma = madamira.process_sentence(candidate.encode('utf-8'))[0].lemma()
                            query_norm = norm.normalize(query, alif=True, hamza=True, yaa=True, tashkil=True)
                            candidate_norm = norm.normalize(candidate, alif=True, hamza=True, yaa=True, tashkil=True)
                            
                            if query_norm != candidate_norm and query_lemma != candidate_lemma:
                                
                                logging.info("Found syn number:" + str(synonym_count))
                                synonym_pairs.append(['syn',query,candidate])
                                synonym_count += 1

            elif antonym_count < antonym_target:
                lookups = thes.thesaurus(query.encode('utf-8'), 'ant', ngram=1, ar=True, target_result_count=1) 
                if 'ant' in lookups:
                    if len(lookups['ant']) > 0:
                        candidate = norm.normalize(lookups['ant'][0], ar_only=True, digits=True, alif=False, hamza=False, yaa=False, tashkil=False).strip('#').strip()
                        if len(candidate) > 1:

                            # make sure the normalized and lemma forms are not the same
                            query_norm = norm.normalize(query, alif=True, hamza=True, yaa=True, tashkil=True)
                            candidate_norm = norm.normalize(candidate, alif=True, hamza=True, yaa=True, tashkil=True)
                            query_lemma = madamira.process_sentence(query.encode('utf-8'))[0].lemma()
                            candidate_lemma = madamira.process_sentence(candidate.encode('utf-8'))[0].lemma()

                            if query_norm != candidate_norm and query_lemma != candidate_lemma:
                                
                                logging.info("Found ant number:"+str(antonym_count))
                                antonym_pairs.append(['ant',query, candidate])
                                antonym_count += 1
            else:
                logging.info("Obtained all word pairs!")
                break

        current_word += 1

if antonym_count < antonym_target or synonym_count < synonym_target:
    logging.info("Ran out of words to draw from!")
else:
    logging.info("Used " + str(current_word) + " of the most frequent words.")

# shuffle and split
current_synonym = 0
current_antonym = 0
tasks = []
for t in range(task_count):
    task = []
    for i in range(int(task_size*synonym_percent)):
        task.append(synonym_pairs[current_synonym])
        current_synonym += 1
    for i in range(int(task_size*antonym_percent)):
        task.append(antonym_pairs[current_antonym])
        current_antonym += 1
    for i in range(int(task_size*shuffle_percent)):
        task.append(['shuf',antonym_pairs[current_antonym][1],synonym_pairs[current_synonym][2]])
        current_antonym += 1
        current_synonym += 1

    # shuffle
    random.shuffle(task)
    tasks.append(task)

# save
for t in range(task_count):
    task = tasks[t]
    with open(taskfile_prefix+str(t)+".txt", 'w') as task_file:
        for pair in task:
            task_file.write(pair[0].encode('utf-8')+', '+pair[1].encode('utf-8')+', '+pair[2].encode('utf-8')+'\n')


