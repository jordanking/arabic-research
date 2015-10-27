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

# random seeding for reproducing
random.seed(1)

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# file to extract most common from
# sourcefile = "/Users/jordanking/Documents/data/arwiki/arwiki-20150901-pages-articles_parsed.txt"
sourcefile = "/Users/jordanking/Documents/data/arwiki/arwiki4k.txt"

# task file prefix
taskfile_prefix = "task_test_"

# max words to draw from in the task
expected_junk = 0.1

# percent of sentences a word must be in to be ignored as a stop word
stopword_thresh = 0.05

# number of task files
task_count = 5
task_size = 250
synonym_percent = 0.5
antonym_percent = 0.25
shuffle_percent = 0.25

synonym_target = task_size*task_count*(synonym_percent+(shuffle_percent/2)+expected_junk)
antonym_target = task_size*task_count*(antonym_percent+(shuffle_percent/2)+expected_junk)
top_n = (synonym_target + antonym_target)*2

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
with open('synonym_task_test.txt', 'w') as task_file:
    # task_file.write("Type,Left,Right,Similarity\n")

    while current_word < top_n:

        if len(norm.normalize(word_list[current_word], ar_only=True, digits=True, alif=False, hamza=False, yaa=False, tashkil=False).strip('#')) > 0:

            if synonym_count < synonym_target:
                lookups = thes.thesaurus(word_list[current_word].encode('utf-8'), 'syn', ngram=1, ar=True, target_result_count=1)
                if 'syn' in lookups:
                    if len(lookups['syn']) > 0:
                        candidate = norm.normalize(lookups['syn'][0], ar_only=True, digits=True, alif=False, hamza=False, yaa=False, tashkil=False).strip('#').strip()
                        if len(candidate) > 1:
                            if word_list[current_word] != candidate:
                                # task_file.write('syn, ')
                                # task_file.write(word_list[current_word].encode('utf-8') + ', ')
                                # task_file.write(candidate.encode('utf-8')+', \n')
                                logging.info("Found syn number:"+ str(synonym_count))
                                synonym_pairs.append([word_list[current_word],candidate])
                                synonym_count += 1

            elif antonym_count < antonym_target:
                lookups = thes.thesaurus(word_list[current_word].encode('utf-8'), 'ant', ngram=1, ar=True, target_result_count=1) 
                if 'ant' in lookups:
                    if len(lookups['ant']) > 0:
                        candidate = norm.normalize(lookups['ant'][0], ar_only=True, digits=True, alif=False, hamza=False, yaa=False, tashkil=False).strip('#').strip()
                        if len(candidate) > 1:
                            if word_list[current_word] != candidate:
                                # task_file.write('ant, ')
                                # task_file.write(word_list[current_word].encode('utf-8') + ', ')
                                # task_file.write(candidate.encode('utf-8')+', \n')
                                logging.info("Found ant number:", str(antonym_count))
                                antonym_pairs.append([word_list[current_word], candidate])
                                antonym_count += 1
            else:
                # we have all our words!
                break

        current_word += 1

    if antonym_count < antonym_target or synonym_count < synonym_target:
        logging.info("Ran out of words to draw from")
    else:
        logging.info("Used " + str(current_word) + " of the most frequent words.")
        logging.info("Done!")

# shuffle and split
current_synonym = 0
current_antonym = 0
for t in range(task_count):
    with open(taskfile_prefix+str(t), 'w') as task_file:
        for i in range(task_size*synonym_percent):
            task_file.write(synonym_pairs[current_synonym][0].encode('utf-8')+', '+synonym_pairs[current_synonym][1].encode('utf-8')+'\n')
            current_synonym += 1
        for i in range(task_size*antonym_percent):
            task_file.write(antonym_pairs[current_antonym][0].encode('utf-8')+', '+antonym_pairs[current_antonym][1].encode('utf-8')+'\n')
            current_antonym += 1
        for i in range(task_size*shuffled_percent/2):
            task_file.write(antonym_pairs[current_antonym][0].encode('utf-8')+', '+synonym_pairs[current_synonym][1].encode('utf-8')+'\n')
            task_file.write(synonym_pairs[current_synonym+1][0].encode('utf-8')+', '+antonym_pairs[current_antonym][1].encode('utf-8')+'\n')

            current_antonym += 1
            current_synonym += 1


# save to files
# with open('synonym_task_test.txt', 'w') as task_file:
#     # task_file.write("Type,Left,Right,Similarity\n")
#     for i in range(len(lhs)):

#         # task_file.write('hidden, ')
#         task_file.write(lhs[i].encode('utf-8') + ', ')
#         task_file.write(rhs[i].encode('utf-8')+', \n')

