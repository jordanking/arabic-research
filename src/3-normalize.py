#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function
from constants import ARAPY_PATH, WORKING_DIRECTORY, PREPROCESSED_DIR, NORMALIZED_DIR
import sys
import os
sys.path.insert(0,ARAPY_PATH)
from arapy.normalization import normalize_sentence_file
from arapy.normalization import normalize
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

# Normalization options
ar_only = True
digits = [True, False]
alif = True
hamza = True
yaa = True
tashkil = [True, False]

for preprocessed in os.listdir(PREPROCESSED_DIR):
    if preprocessed = "pos.txt":
        continue
    for digit_option in digits:
        for tashkil_option in tashkil:
            logging.info("Normalizing dump")
            outfile = NORMALIZED_DIR+"/"+preprocessed[:-4]+"dig"+str(digit_option)+"tash"+str(tashkil_option)+".txt"
            normalized_file = normalize_sentence_file(PREPROCESSED_DIR+"/"+preprocessed,
                                                      outfile_path = outfile,
                                                      ar_only = ar_only,
                                                      digits = digit_option,
                                                      alif = alif,
                                                      hamza = hamza,
                                                      yaa = yaa,
                                                      tashkil = tashkil_option)
logging.info("Done!")