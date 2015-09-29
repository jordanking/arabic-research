time /Users/king96/Applications/word2vec/word2vec \
-train /Users/king96/Documents/Data/Wiki/en_wiki_9.txt \
-output /Users/king96/Documents/Word2Vec/Models/en_wiki_c_vectors.bin \
-cbow 1 \
-size 200 \
-window 8 \
-negative 25 \
-hs 0 \
-sample 1e-4 \
-threads 20 \
-binary 1 \
-iter 15

