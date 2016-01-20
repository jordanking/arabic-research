#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function

import sys
# sys.path.insert(0,"/home/jordan/Documents/Projects/")
sys.path.insert(0,"/Users/jordanking/Documents/")

from arapy.arwiki import parse_arwiki_dump
from arapy.madamira import transform_sentence_file
from arapy.normalization import normalize_sentence_file
from arapy.normalization import normalize
from arapy.word2vec import train_embeddings
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)


embeddings_destination = "/Users/jordan/Documents/Projects/arabic-research/vecs/"

# wiki_file = "/media/jordan/Media/data/arabic/arwiki-20150901-pages-articles.xml"
wiki_file = "/Users/jordanking/Documents/data/arwiki/arwiki-20150901-pages-articles.xml"
parse_file = ""
lemma_file = ""
token_file = ""
pos_file = ""

# if NLP options should be reparsed
preprocessed = False

# Normalization options
ar_only = True
digits = [True]#, False]
alif = True
hamza = True
yaa = True
tashkil = [True]#, False]

# Word2Vec parameter options
sg = [0]#, 1]
size = [100]#, 200]
window = [4]#,7]
min_count = 5
sample = 1e-5
seed = 18
hs = 1
negative = 0
iterations = 5

if not preprocessed:
    logging.info("Parsing dump.")
    parse_file = parse_arwiki_dump(wiki_file, split_at_punc=True, remove_non_arabic=True)

    logging.info("Obtaining Lemmas, POS, and Tokens")
    lemma_file, pos_file, token_file = transform_sentence_file(parse_file, lemmas=True, pos=True, tokens=True)

nlp_types = [parse_file]#, lemma_file, token_file]

for nlp_option in nlp_types:
    for digit_option in digits:
        for tashkil_option in tashkil:

            logging.info("Normalizing dump")
            normalized_file = normalize_sentence_file(nlp_option, 
                                                     ar_only = ar_only,
                                                     digits = digit_option,
                                                     alif = alif,
                                                     hamza = hamza,
                                                     yaa = yaa,
                                                     tashkil = tashkil_option)

            for model_option in sg:
                for size_option in size:
                    for window_option in window:

                      logging.info("Generating word vectors")
                      embeddings_file = train_embeddings(normalized_file, 
                                                         embeddings_destination,
                                                         sg = model_option,
                                                         size = size_option,
                                                         window = window_option,
                                                         min_count = min_count,
                                                         sample = sample,
                                                         seed = seed,
                                                         hs = hs,
                                                         negative = negative,
                                                         iter = iterations)

                    # pos evaluation

                    # semantic task

                    # other task?

logging.info("Done!")