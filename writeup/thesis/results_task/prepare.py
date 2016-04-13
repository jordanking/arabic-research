import pandas as pd

sort_metric = 'Correlation'

files = ['/Users/jordanking/Documents/arabic-research/writeup/thesis/results_task/four_corr.csv',
         '/Users/jordanking/Documents/arabic-research/writeup/thesis/results_task/three_corr.csv',
         '/Users/jordanking/Documents/arabic-research/writeup/thesis/results_task/two_corr.csv']

# for file in files:
#     df = pd.read_csv(file)
#     
av = sum([0.675289665616538,0.6626460660772577,0.6354635507101805,0.7639366027218167,0.7511178003615244,0.7249475689109525]) / 6


print(av)