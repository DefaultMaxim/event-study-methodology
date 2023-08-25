from prepate_data import prepare_data
from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd


token_path = 'token.txt'

with open(token_path) as f:
    token = f.readlines()

token = token[0]

fig_path = 'share_figi.txt'

close_portfolio, change_portfolio, log_change_portfolio, shares_list = prepare_data(token=token, fig_file=fig_path)

close_portfolio.to_csv('datasets/close_portfolio.csv')
change_portfolio.to_csv('datasets/change_portfolio.csv')
log_change_portfolio.to_csv('datasets/log_change_portfolio.csv')

for i in range(len(shares_list)):
    shares_list[i].to_csv(f'datasets/share{i}.csv')
