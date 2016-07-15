import pandas as pd

sort_metric = 'Correlation'

files = ['/Users/jordanking/Documents/arabic-research/writeup/thesis/results/ar_similiarity_task_results.csv',
		 '/Users/jordanking/Documents/arabic-research/writeup/thesis/results/ar_similiarity_task_results_ws353.csv',
		 '/Users/jordanking/Documents/arabic-research/writeup/thesis/results/en_similarity_task_results.csv']

for file in files:
	df = pd.read_csv(file)
	df = df.sort_values(by=sort_metric)
	df = df.round({'Accuracy':3, 'MSE':3, 'Correlation':3})
	df.to_csv(file[:-4]+'_sorted_' + sort_metric + '.csv', index=False)