from tinkoff.invest import CandleInterval, Client
from datetime import timedelta
from tinkoff.invest.utils import now
import warnings


warnings.filterwarnings('ignore')


def tink_get_data(token: str, fig_file):
    """ Загружает данные из тинька по фиги кодам из .txt файла, фиги разделены запятыми.
        возвращает список акций для дальнейшей работы"""
    TOKEN = token
    fig_file = 'share_figi.txt'

    with Client(TOKEN) as client:
        print(client.users.get_accounts())

    with open(fig_file) as f:
        row = f.readlines()
    figs = row[0].split(", ")

    shares = [[] for _ in range(len(figs))]

    for key, fig in enumerate(figs):

        with Client(TOKEN) as client:

            for candle in client.get_all_candles(

                    figi=fig,

                    from_=now() - timedelta(days=365),

                    interval=CandleInterval.CANDLE_INTERVAL_HOUR,
            ):
                shares[key].append(candle)

    return shares, figs
