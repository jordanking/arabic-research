#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function

import sys

sys.path.insert(0,"/Users/jordanking/Documents/")
import arapy.thesaurus as thes

for word, rel in thes.thesaurus('ملك', 'syn', 0, 1):
    print(word, rel)