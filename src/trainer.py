#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

from gensim.models import Word2Vec
import logging
import sys



def main():
    if (len(sys.argv) < 2):
        print("Please use this script with an input path and output path as args.")
        print("In: Text file with 1 sentence per line")
        print("Out: Binary word vector file")

    infile = sys.argv[1]
    outfile = sys.argv[2]

    print("Files opened!")
    
    # set up logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

    class MySentences(object):
        def __init__(self, fname):
            self.fname = fname
            self.errors = 0

        def __iter__(self):
            for line in open(self.fname):
                yield line.split()

    sentences = MySentences(infile)

    """
    Initialize the model from an iterable of `sentences`. Each sentence is a
    list of words (unicode strings) that will be used for training.

    The `sentences` iterable can be simply a list, but for larger corpora,
    consider an iterable that streams the sentences directly from disk/network.
    See :class:`BrownCorpus`, :class:`Text8Corpus` or :class:`LineSentence` in
    this module for such examples.

    If you don't supply `sentences`, the model is left uninitialized -- use if
    you plan to initialize it in some other way.

    `sg` defines the training algorithm. By default (`sg=1`), skip-gram is used. Otherwise, `cbow` is employed.

    `size` is the dimensionality of the feature vectors.

    `window` is the maximum distance between the current and predicted word within a sentence.

    `alpha` is the initial learning rate (will linearly drop to zero as training progresses).

    `seed` = for the random number generator. Initial vectors for each
    word are seeded with a hash of the concatenation of word + str(seed).

    `min_count` = ignore all words with total frequency lower than this.

    `sample` = threshold for configuring which higher-frequency words are randomly downsampled;
        default is 0 (off), useful value is 1e-5.

    `workers` = use this many worker threads to train the model (=faster training with multicore machines).

    `hs` = if 1 (default), hierarchical sampling will be used for model training (else set to 0).

    `negative` = if > 0, negative sampling will be used, the int for negative
    specifies how many "noise words" should be drawn (usually between 5-20).

    `cbow_mean` = if 0 (default), use the sum of the context word vectors. If 1, use the mean.
    Only applies when cbow is used.

    `hashfxn` = hash function to use to randomly initialize weights, for increased
    training reproducibility. Default is Python's rudimentary built in hash function.

    `iter` = number of iterations (epochs) over the corpus.
    """
    model = Word2Vec(sentences, sg = 0, size = 100, window = 8, 
                     min_count = 5, hs = 0, workers = 4, sample = 1e-4, 
                     negative = 25, iter = 15)

    #model.save(outfile + '.pbin')

    model.save_word2vec_format(outfile, binary = True)

if __name__ == "__main__":
    main()