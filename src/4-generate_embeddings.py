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
# EMBEDDING_DIR = '/home/jordan/Documents/Projects/arabic-research/temp/4-1-embeddings'

# Word2Vec parameter options
sg = [0, 1]
# sg = [1]
size = [100, 200]
# size = [100]
window = [4,7]
# window = [4]
min_count = 5
sample = 1e-5
seed = 18
hs = 1
negative = 0
iterations = 5

skip = 46
stop_after  = 47
count = 0

for normalized in os.listdir(NORMALIZED_DIR):
    for model_option in sg:
        for size_option in size:
            for window_option in window:
                count+=1
                if (count > stop_after):
                    sys.exit(0)
                if (count > skip):
                    logging.info("Generating word vectors")
                    outfile = EMBEDDING_DIR+"/"+normalized[:-4]+"mod"+str(model_option)+"size"+str(size_option)+"wind"+str(window_option)+".txt"

                    embeddings_file = train_embeddings(NORMALIZED_DIR+"/"+normalized,
                                                       outfile = outfile, 
                                                       sg = model_option,
                                                       size = size_option,
                                                       window = window_option,
                                                       min_count = min_count,
                                                       sample = sample,
                                                       seed = seed,
                                                       hs = hs,
                                                       negative = negative,
                                                       iterations = iterations)
                else:
                    outfile = EMBEDDING_DIR+"/"+normalized[:-4]+"mod"+str(model_option)+"size"+str(size_option)+"wind"+str(window_option)+".txt"
                    print('skipping %s' % (outfile))
logging.info("Done!")