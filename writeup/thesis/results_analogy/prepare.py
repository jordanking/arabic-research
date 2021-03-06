import pandas as pd
import matplotlib.pyplot as plt

sort_metric = 'Scores'

files = ['/Users/jordanking/Documents/arabic-research/writeup/thesis/results_analogy/ar_analogy_results_fixed.csv']

def parseParameters(filename):
    #controldigTruetashTruemod1size200wind7.txt
    params = {}
    preprocessing_options = ['control', 'lemmas', 'tokens']
    for opt in preprocessing_options:
        if filename.startswith(opt):
            params['preprocessing'] = opt
            filename = filename[len(opt):]
    normalization_options = ['dig', 'tash']
    for opt in normalization_options:
        filename = filename[len(opt):]
        if filename.startswith('True'):
            params[opt] = True
            filename = filename[4:]
        else:
            params[opt] = False
            filename = filename[5:]
    model_options = ['mod', 'size', 'wind']
    for opt in model_options:
        filename = filename[len(opt):]
        value = ''
        for char in filename:
            if char.isdigit():
                value += char
            else:
                break
        params[opt] = int(value)
        filename = filename[len(value):]
    return params

for file in files:
    df = pd.read_csv(file)
  
    for index, row in df.iterrows():
        params = parseParameters(row.at['Embedding File'])

        # rename control to base
        if params['preprocessing'] == 'control':
            params['preprocessing'] = 'base'

        df.set_value(index, 'wind', int(params['wind']))
        df.set_value(index, 'size', int(params['size']))
        df.set_value(index, 'mod', int(params['mod']))
        df.set_value(index, 'dig', params['dig'])
        df.set_value(index, 'tash', params['tash'])
        df.set_value(index, 'preprocessing', params['preprocessing'])
        df.set_value(index, 'preprocessing_abbr', params['preprocessing'][0].upper())
    df['rank'] = df['Scores'].rank(ascending=False).astype(int)
    df['wind'] = df['wind'].astype(int)
    df['size'] = df['size'].astype(int)
    df['mod'] = df['mod'].astype(int)

    plot = df.boxplot(column='Scores', by=['size','preprocessing_abbr'])
    plt.title("Grouped by Vector Size and Preprocessing Method")
    plt.xlabel('Size,Preprocessing (B: Base, L: Lemmas, T: Tokens)')
    plt.annotate('B: Base\n L: Lemmas\n T: Tokens', xy=(-12, -12), xycoords='axes points',
            size=14, ha='right', va='top',
            bbox=dict(boxstyle='round', fc='w'))
    plt.suptitle("")
    # plt.show()
    plt.savefig(file[:-4] + '_plot.png')


    df = df.sort_values(by=sort_metric, ascending=False)
    df = df.round({'Hit_Percent':4, 'Scores':4})
    df = df.drop('preprocessing_abbr', 1)
    df = df.head(10)

    df.to_csv(file[:-4]+'_prepared' + '.csv', index=False)
  
    


