import investpy
import time
from datetime import datetime, timedelta
from rsi import get_rsi
from macd import get_macd
import pandas as pd
from tabulate import tabulate
from sendgrid_handler import send_email


def get_data(share_name, days=30):
    today = datetime.today().strftime("%d/%m/%Y")
    start_date = datetime.today() - timedelta(days=days)
    start_date = start_date.strftime("%d/%m/%Y")

    df = investpy.get_stock_historical_data(stock=share_name,
                                            country='sri lanka',
                                            from_date=start_date,
                                            to_date=today)

    return df


if __name__ == '__main__':
    shares = ['SAMP', 'JKH', 'CTC', 'HNB', 'NDB', 'LLUB', 'EXPO', 'BRWN', 'DIAL', 'DIPD', 'HHL',
              'HAYL', 'RICH', 'RCL', 'LOLC', 'LFIN', 'MELS', 'TEEJ', 'VALI']

    while True:
        days_from_beginning = int(time.time()/(24 * 60 * 60))
        start_of_next_day = (days_from_beginning + 1) * 24 * 60 * 60
        time.sleep(start_of_next_day - time.time() - 5.5*60*60)

        data = {'Stock': [],
                'RSI': [],
                'MACD': [],
                'Signal': [],
                'Diff': [],
                ' ': []}
        for share in shares:
            df = get_data(share)
            RSI = get_rsi(df.Open.to_numpy(), df.Close.to_numpy())
            macd, signal, diff = get_macd(share)

            data['Stock'].append(share)
            data['RSI'].append(round(RSI))
            data['MACD'].append(macd)
            data['Signal'].append(signal)
            data['Diff'].append(diff)
            data[' '].append('buy' if macd > signal else 'sell')

        df = pd.DataFrame(data=data)
        df = df.sort_values(by=['RSI'])
        send_email(df.to_html(), title="Stock Market Update")

        time.sleep(60)
