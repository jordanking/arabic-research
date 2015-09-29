import sys

# add the path of arapy
sys.path.insert(0,"/home/jordan/Documents/Projects/")
from arapy.util import parse_wiki_dump

"""
This code takes in and out args for a wiki xml dump in, 
and normalized arabic sentences out.
"""

parse_wiki_dump(sys.argv[1], sys.argv[2], True)