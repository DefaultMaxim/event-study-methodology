import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.linear_model import LinearRegression

change_df = pd.read_csv('datasets/change_portfolio.csv', index_col='time')
change_df['idx'] = [i for i in range(len(change_df))]

close_df = pd.read_csv('datasets/close_portfolio.csv', index_col='time')
close_df['idx'] = [i for i in range(len(close_df))]

log_change_df = pd.read_csv('datasets/log_change_portfolio.csv', index_col='time')
log_change_df['idx'] = [i for i in range(len(log_change_df))]

shares_dfs = []

for i in range(5):
    shares_dfs.append(pd.read_csv(f'datasets/share{i}.csv', index_col='time'))

# нужно получить кэфы b0 и b1 из ур-я $E(R_{i, t})  = b_0 + b_1 \cdot E(R_{M, t})$,
# где $E(R_{M, t})$ - средняя доходность портфеля (рынка),
# их можно получить из ур-я регрессии, взяв данные до -20 дня до event
# как только получили их можно продолжать

avg_market_return = change_df.mean().mean()
event_idx = change_df.loc[[str(pd.to_datetime('2023-06-23 19:00:00+00:00'))]].idx.values[0]
horizon_idx = event_idx - 20

# кароче че доделать мб создать колонку со средними доходами (каждый день обновляется же)
# потом построить регрессию х - мб число, мб много чиселок просто, пробуй,
# дальше по алгоритму

display(change_df.iloc[:, 0][:horizon_idx])
y = [change_df.iloc[:, j][:i].mean() for i in range(horizon_idx) for j in range(len(change_df.columns) - 1)]
X = [change_df[:i].mean().mean() for i in range(horizon_idx)]

#display(y)
display(X)
print(len(change_df.columns))
display(change_df.columns)
