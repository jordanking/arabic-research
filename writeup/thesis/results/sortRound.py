import pandas as pd

files = ['/Users/jordanking/Documents/arabic-research/writeup/acl2016/results/preprocessing_eval.csv',
		 '/Users/jordanking/Documents/arabic-research/writeup/acl2016/results/preprocessing_eval_1.csv',
		 '/Users/jordanking/Documents/arabic-research/writeup/acl2016/results/en_sim_demo.csv']

for file in files:
	df = pd.read_csv(file)
	df = df.sort_values(by='Accuracy')
	df = df.round({'Accuracy':3, 'MSE':3, 'Correlation':3})
	df.to_csv(file[:-4]+'_sorted.csv', index=False)