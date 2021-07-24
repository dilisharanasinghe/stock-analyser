import pandas as pd
import numpy as np
import investpy
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


def get_data(share_name, days=365):
    today = datetime.today().strftime("%d/%m/%Y")
    start_date = datetime.today() - timedelta(days=days)
    start_date = start_date.strftime("%d/%m/%Y")

    df = investpy.get_stock_historical_data(stock=share_name,
                                            country='sri lanka',
                                            from_date=start_date,
                                            to_date=today)

    return df


def __get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span=fast, adjust=False).mean()
    exp2 = price.ewm(span=slow, adjust=False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns={'Close': 'macd'})
    signal = pd.DataFrame(macd.ewm(span=smooth, adjust=False).mean()).rename(columns={'macd': 'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns={0: 'hist'})
    frames = [macd, signal, hist]
    df = pd.concat(frames, join='inner', axis=1)
    return df


def get_macd(share_name, enable_plot=False):
    df = get_data(share_name)
    data = __get_macd(df.Close, 26, 12, 9)

    if enable_plot:
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.plot(df.Close)
        ax2.plot(data.macd)
        ax2.plot(data.signal)
        plt.show()

    # print(data.iloc[[-1]]['macd'])
    # print(data['macd'][-1], data['signal'][-1])

    return data['macd'][-1], data['signal'][-1], data['hist'][-1]


if __name__ == '__main__':
    get_macd('EXPO', enable_plot=True)
