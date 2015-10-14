#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function

import sys
import gensim
import logging

import re
from collections import Counter

sys.path.insert(0,"/Users/jordanking/Documents/")
import arapy.thesaurus as thes

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# file to extract most common from
sourcefile = "/Users/jordanking/Documents/data/arwiki/arwiki-20150901-pages-articles_parsed.txt"

# how many words to use in the task
top_n = 4000
synonym_target = 800
antonym_part = 200

synonym_count = 0
antonym_count = 0

logging.info("Building dictionary of top words")

# get most common words that don't appear in more than five percent of the sentences
document = gensim.corpora.dictionary.Dictionary()
with open(sourcefile, 'r') as doc_file:
    for line in doc_file:
        document.doc2bow(line.split(), allow_update=True)
document.filter_extremes(no_below=5, no_above=0.05, keep_n=top_n)

id_list=document.keys()
word_list = document.values()
for val in word_list:
    print(val)

# # word_list = most_common_words(text_source, top_n, skip_stop_words)
current_word = 0

lhs = []
rhs = []
with open('synonym_task.txt', 'w') as task_file:
    task_file.write("Left,Right,Similarity\n")


    while current_word < top_n:

        if synonym_count < synonym_target:
            lookups = thes.thesaurus(word_list[current_word].encode('utf-8'), 'syn', ngram=1, ar=True, trans_with_google=True, target_result_count=1)
            if 'syn' in lookups:
                if len(lookups['syn']) > 0:
                    # lhs.append(word_list[current_word])
                    task_file.write(word_list[current_word].encode('utf-8') + ', ')
                    # rhs.append(lookups['syn'][0])
                    task_file.write(lookups['syn'].encode('utf-8')+', \n')
                    synonym_count += 1

        elif antonym_count < antonym_target:
            lookups = thes.thesaurus(word_list[current_word].encode('utf-8'), 'ant', ngram=1, ar=True, trans_with_google=True, target_result_count=1) 
            if 'ant' in lookups:
                if len(lookups['ant']) > 0:
                    task_file.write(word_list[current_word].encode('utf-8') + ', ')
                    task_file.write(lookups['ant'].encode('utf-8')+', \n')
                    # lhs.append(word_list[current_word])
                    # rhs.append(lookups['ant'][0])
                    antonym_count += 1
        else:
            # we have all our words!
            break

        current_word += 1