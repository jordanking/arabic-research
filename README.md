# Arabic Research
Research into the production of arabic word vectors, on the effects of preprocessing, normalization, and word2vec parameterization. See the paper at [some site someday].

# Pipeline - src directory

There are six main steps in the pipeline. These cover everything to train, evaluate and apply arabic word embeddings.

1: The first pipeline step is to parse wikipedia. There are two scripts in src, one to parse english wiki and one to parse arabic wiki. The wiki dumps are available in compressed form straight from wikipedia.

2: The second step is to preprocess the text obtained. This is when lemmas and tokens are obtained. The script is also set up to obtain part of speech tags for each word.

3: The third step normalizes the arabic text in various optional ways, notably mapping numerics to the # symbol and removing arabic voweling

4: The fourth step trains the embeddings. One file is for the whole parameter sweep in arabic, the repair embeddings script is for training a single model if something goes wrong, and the other script is for training english word embeddings.

5: The fifth step evaluates the embeddings using similarity and analogy tasks. One script does arabic similarity task evaluations, one does english similarity task evaluations, and one does analogy evaluation for either language (needs hardcoded parameterization)

6: The final step uses word embeddings in different ways to measure buzz. The version marked intense uses the expensive average similarity method that turns out to be most effective. The other two are set up for other methods. The intense version's average similarity should be the main focus here, all of these scripts are pretty sloppy code done in a rush and not yet repaired.

Constants: There is a file labeled constants.py that is referenced by most of the pipeline steps. This should be set up before running anything.

ARAPY_PATH = location of my arabic processing python package
WORKING_DIRECTORY = location to stage the directories for each pipeline step (see below)

WIKI_FILE = wikipedia source

PARSE_FILE = what to call wiki text
LEMMA_FILE = name of lemma file
TOKEN_FILE = name of token file
POS_FILE = part of speech labels
CONTROL_FILE = copy of parsed dir
PREPROCESSED_DIR = directory containing the above group of preprocessed text

NORMALIZED_DIR = directory name for 3rd step
EMBEDDING_DIR = directory name for 4th step
RESULTS_DIR = directory name for 5th step

TASKS = list of similarity task files
AR_SIM_OUTPUT_FILES = list of names corresponding to the results for the above list
ANALOGY_TASKS = list of analogy task files
ANALOGY_OUTPUT_FILES = list of result files for above analogy list           
ANALOGY_OUT_HEADER = for analogy result file csv
EN_SIM_OUTPUT_FILE = file for english similarity
IN_HEADER = header of similarity tasks
OUT_HEADER = header for similarity task output file

# analogy_tasks directory

This contains the original analogy task list from the original word2vec paper. It also contains a script for translating to arabic, and a script for converting unicode encoded arabic to arabic script

# buzz directory

This contains support files for the sixth step of the pipeline. There is an expert domain list of words related to violence in arabic, one expanded with synonyms (doesn't work well?), the ground truth months from the iraq death count site, master output files from buzz methods (not necessarily up-to-date results) and a directory of results for each individual method of buzz detection. More up-to-date results can be found in the writeup/thesis/buzz_results directory.

# semantic_tasks directory

The mine directory has all of the results I collected from native arabic speakers. The mine/originals directory has the unlabeled word pairs. In /mine/ there is a script to merge the results. It rescales and averages the various collected results.

The /others directory has the ws353 task in it, and another I didn't use. There is a script that I used to separate out the arabic and english tasks to the format my pipeline takes.

# temp

The temp directory is set up to hold the processed text and models. The structure should match what is found in the src/constants.py file, of one directory per pipeline step.

# writeup

This contains my thesis work currently. There are up-to-date copies of my results in directories within writeup/thesis/, and the paper explains the results and motivations of my work.