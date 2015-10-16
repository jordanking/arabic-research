#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import logging
import sys

sys.path.insert(0,"/Users/jordanking/Documents/")

taskfile = 'synonym_task_filtered.txt'
resultfile = 'test_results.txt'

with open(taskfile, 'r') as task_file:
    with open(resultfile, 'w') as results:
        for line in task_file:
            relation, lhs, rhs, similarity = line.split(',')
            print(relation, lhs, rhs)
            similarity = input('How similar are the two above words? ')
            results.write(relation)
            results.write(lhs)
            results.write(rhs)
            results.write(str(similarity))