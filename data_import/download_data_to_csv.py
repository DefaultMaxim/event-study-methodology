from prepate_data import prepare_data
from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('TOKEN')

fig_path = 'share_figi.txt'

close_portfolio, change_portfolio, log_change_portfolio, shares_list = prepare_data(token=token, fig_file=fig_path)

close_portfolio.to_csv('datasets/close_portfolio.csv')
change_portfolio.to_csv('datasets/change_portfolio.csv')
log_change_portfolio.to_csv('datasets/log_change_portfolio.csv')

for i in range(len(shares_list)):
    shares_list[i].to_csv(f'datasets/share{i}.csv')
