#!/usr/bin/env python
# coding: utf-8

# ARAPY_PATH = "/home/jordan/Documents/Projects/"
# WORKING_DIRECTORY = "/home/jordan/Documents/Projects/arabic-research/temp"
# NORMALIZED_DIR = WORKING_DIRECTORY+"/3-normalized"
# EMBEDDING_DIR = WORKING_DIRECTORY+"/4-embeddings"

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
from constants import ARAPY_PATH, WORKING_DIRECTORY, NORMALIZED_DIR, EMBEDDING_DIR
import sys
import os
sys.path.insert(0,ARAPY_PATH)
from arapy.word2vec import train_embeddings
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# Word2Vec parameter options
english_text = '/media/jordan/Media/data/enwiki/english_training_9mil'
english_model = '/home/jordan/Desktop/english_9mil.bin'



sg = [1]
size = [100]
window = [7]
min_count = 5
sample = 1e-3
seed = 1
hs = 1
negative = 0
iterations = 5


for model_option in sg:
    for size_option in size:
        for window_option in window:

            logging.info("Generating word vectors")
            outfile = english_text[:-4]+"mod"+str(model_option)+"size"+str(size_option)+"wind"+str(window_option)+".txt"

            embeddings_file = train_embeddings(english_text,
                                               outfile = english_model, 
                                               sg = model_option,
                                               size = size_option,
                                               window = window_option,
                                               min_count = min_count,
                                               sample = sample,
                                               seed = seed,
                                               hs = hs,
                                               negative = negative,
                                               iterations = iterations)

logging.info("Done!")

#collected 799096 word types from a corpus of 124556873 words and 8809542 sentences
#2016-03-18 16:15:25,903 : INFO : min_count=5 retains 162553 unique words (drops 636543)
#collected 3294264 word types from a corpus of 215496872 words and 9000000 sentences
#2016-03-19 18:47:01,073 : INFO : min_count=5 retains 495229 unique words (drops 2799035)
