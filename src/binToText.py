from gensim.models import word2vec


modelfile = raw_input('Please enter the binary model file path: ')
modelfile = modelfile.strip().strip('\'')

model = word2vec.Word2Vec.load_word2vec_format(modelfile, binary=True)
model.save_word2vec_format(modelfile[:-4]+'.embedding', binary=False)
