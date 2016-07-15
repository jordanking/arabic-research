#!/usr/bin/env python
# coding: utf-8

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
infile = '/home/jordan/Documents/Projects/arabic-research/temp/3-normalized/lemmasdigFalsetashFalse.txt'
outfile = '/home/jordan/Desktop/arabic_embedding.bin'

sg = 1
size = 100
window = 7
min_count = 5
sample = 1e-5
seed = 18
hs = 1
negative = 0
iterations = 5



logging.info("Generating word vectors")
# outfile = EMBEDDING_DIR+"/"+normalized[:-4]+"mod"+str(model_option)+"size"+str(size_option)+"wind"+str(window_option)+".txt"

embeddings_file = train_embeddings(infile,
                                   outfile = outfile, 
                                   sg = sg,
                                   size = size,
                                   window = window,
                                   min_count = min_count,
                                   sample = sample,
                                   seed = seed,
                                   hs = hs,
                                   negative = negative,
                                   iterations = iterations)

logging.info("Done!")

#collected 799096 word types from a corpus of 124556873 words and 8809542 sentences
#2016-03-18 16:15:25,903 : INFO : min_count=5 retains 162553 unique words (drops 636543)

# collected 710715 word types from a corpus of 88672990 words and 8809542 sentences
# 2016-03-20 02:55:52,231 : INFO : min_count=5 retains 115312 unique words (drops 595403)
# 2016-03-20 02:55:52,231 : INFO : min_count leaves 87828019 word corpus (99% of original 88672990)
