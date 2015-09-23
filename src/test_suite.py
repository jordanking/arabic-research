from gensim.models import Word2Vec
import logging

def main():
    output_spacing = 25

    modelfile = raw_input('Please enter the binary model file path (or gn/en/ar): ')
    modelfile = modelfile.strip()

    if modelfile == 'gn':
        modelfile = '/Users/king96/Documents/Word2Vec/Models/google_news_vecs.bin'
    elif modelfile == 'ar':
        modelfile = '/Users/king96/Documents/Word2Vec/Models/ar_wiki_seg_vecs.bin'
    elif modelfile == 'en':
        modelfile = '/Users/king96/Documents/Word2Vec/Models/en_wiki_vecs.bin'

    # set up logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    # load model
    model = Word2Vec.load_word2vec_format(modelfile, binary=True)

    while True:
        
        print '\n'
        print 'Type ac to run accuracy tests.'
        print 'Enter one word for neighbors, two for distance,'
        print 'three for analogy, more for matching, q to quit.'
        words = raw_input('Word: ')

        words = words.decode('UTF-8', 'replace')
        
        if words == 'q':
            break

        if words == 'ac':
            print 'Please enter the questions file to test on:'

            questions = raw_input('File: ').strip()

            model.accuracy(questions, restrict_vocab = 30000, tries = 5)
            continue

        # the remaining options take 0 < n query words
        words = words.split(' ')

        if len(words) == 0:
            continue

        # top 10 words
        elif len(words) == 1:
            try:
                candidates = model.most_similar(words[0], topn=10)
                print 'Candidates'.rjust(output_spacing), 'Cos Distance'.rjust(output_spacing)
                for word in candidates:
                    print str(word[0].encode('UTF-8','replace')).rjust(output_spacing), str(word[1]).rjust(output_spacing)
            except KeyError as ke:
                print ke.message.encode('utf-8','replace')


        # pair similarity
        elif len(words) == 2:
            try:
                print 'Similarity is : ' + str(model.similarity(words[0],words[1]))
            except KeyError as ke:
                print ke.message.encode('utf-8','replace')

        # analogy
        elif len(words) == 3:
            try:
                candidates = model.most_similar(positive=[words[2], words[1]], 
                                                negative = [words[0]], 
                                                topn=10)

                print 'Candidates'.rjust(output_spacing), 'Cos Distance'.rjust(output_spacing)
                for word in candidates:
                    print str(word[0].encode('UTF-8', 'replace')).rjust(output_spacing), str(word[1]).rjust(output_spacing)
            except KeyError as ke:
                print ke.message.encode('utf-8','replace')

        # odd one out
        else:
            try:
                print 'Odd one out: ' + str(model.doesnt_match(words).encode('utf-8', 'replace'))
            except KeyError as ke:
                print ke.message.encode('utf-8','replace')


if __name__ == "__main__":
    main()