from gensim.models import Word2Vec
import logging

modelfile = raw_input('Please enter the binary model file path (gn for google news): ')
modelfile = modelfile.strip()

if modelfile == 'gn':
    modelfile = '/Users/king96/Documents/Word2Vec/Models/google_news_vecs.bin'

# set up logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

# load model
model = Word2Vec.load_word2vec_format(modelfile, binary=True)

while True:
    
    print 
    words = raw_input('\nEnter words to expand, q to quit: ')

    words = words.decode('UTF-8', 'replace')
    
    if words == 'q':
        break

    words = words.split(' ')

    if len(words) == 0:
        continue

    # top 10 words
    else:
        expansion = set()

        for word in words:
            try:
                expansion = expansion | set([x[0] for x in model.most_similar(word, topn=10)])
            except KeyError as ke:
                print ke.message.encode('utf-8','replace')

        print 'Expansion'
        for word in expansion:
            print str(word.encode('UTF-8','replace'))
