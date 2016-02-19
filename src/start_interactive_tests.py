# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function

import sys
sys.path.insert(0,"/home/jordan/Documents/Projects/")

from arapy.word2vec import start_interactive_test_suite
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

start_interactive_test_suite()