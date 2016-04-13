import pandas as pd

sort_metric = 'Spearman'

files = ['/Users/jordanking/Documents/arabic-research/writeup/thesis/results_spearman/ar_similiarity_task_multi_results.csv',
         '/Users/jordanking/Documents/arabic-research/writeup/thesis/results_spearman/ar_similiarity_task_results_ws353.csv',
         '/Users/jordanking/Documents/arabic-research/writeup/thesis/results_spearman/ar_similiarity_task_results.csv']#,
         # '/Users/jordanking/Documents/arabic-research/writeup/thesis/results_spearman/ar_similiarity_task_4_results.csv']


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

        df.set_value(index, 'wind', int(params['wind']))
        df.set_value(index, 'size', int(params['size']))
        df.set_value(index, 'mod', int(params['mod']))
        df.set_value(index, 'dig', params['dig'])
        df.set_value(index, 'tash', params['tash'])
        df.set_value(index, 'preprocessing', params['preprocessing'])
    
    df['wind'] = df['wind'].astype(int)
    df['size'] = df['size'].astype(int)
    df['mod'] = df['mod'].astype(int)

    df = df.sort_values(by=sort_metric, ascending=False)
    df = df.round({'Accuracy':4, 'MSE':4, 'Correlation':4})

    # df = df.head(10)

    df.to_csv(file[:-4]+'_prepared' + '.csv', index=False)


