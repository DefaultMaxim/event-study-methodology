from get_data import tink_get_data
from format_data import create_df
from get_ticker_by_figi import figi_to_ticker
from IPython.display import display

token='t.0aEb3hkZKL2AuMukVswlOk0aRKkPfGAi6Gd6dD8stZAC9xQX8gJrBwR-8vBO83xDkmObgdX6lPq7AhorkbhiTg'
fig_file='share_figi.txt'

shares_list, figis = tink_get_data(token=token,
                                   fig_file=fig_file)

for i in range(len(shares_list)):
    shares_list[i] = create_df(shares_list[i])

for i in range(len(shares_list)):
    if shares_list[i] is not None:
        display(i, shares_list[i])
