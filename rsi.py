import investpy
import numpy as np
import datetime
from matplotlib import pyplot as plt
import pandas as pd


def get_ewm(data, newest_first=False):
    window = data.shape[0]
    alpha = 2 /(window + 1.0)

    r = np.arange(window)
    if not newest_first:
        r = np.flip(r)
    # print(r, window)
    scale_arr = (1-alpha)**r

    out = alpha * data * scale_arr
    out = np.sum(out)
    return out


def get_rsi(open_prices, close_prices):
    difference = close_prices - open_prices
    difference = difference[-14:]

    # gains = difference[difference >= 0]
    # losses = difference[difference < 0]
    #
    # avg_gains = np.sum(gains) / 14
    # avg_losses = np.sum(np.abs(losses)) / 14

    # print('RS1', avg_gains/avg_losses)
    gains = []
    losses = []

    for d in range(difference.shape[0]):
        if difference[d] > 0:
            gains.append(difference[d])
            losses.append(0)
        else:
            losses.append(abs(difference[d]))
            gains.append(0)

    avg_gains = get_ewm(np.array(gains))
    avg_losses = get_ewm(np.array(losses))

    # print('RS2', avg_gains / avg_losses)
    if avg_losses == 0:
        RS = 0.0001
    else:
        RS = avg_gains / avg_losses

    RSI = 100 - (100 / (1 + RS))

    return RSI


def evaluate(share_name, start_date='01/01/2020', enable_graphs=False):
    today = datetime.datetime.today().strftime("%d/%m/%Y")

    df = investpy.get_stock_historical_data(stock=share_name,
                                            country='sri lanka',
                                            from_date=start_date,
                                            to_date=today)

    RSIs = []
    buys = []
    num_of_shares = []
    default_buy = 2000

    def get_avg_share_price():
        a = 0
        # print(buys, num_of_shares)
        for i in range(len(buys)):
            a += buys[i] * num_of_shares[i]

        return a / np.sum(num_of_shares)

    for i in range(14, df.shape[0]):
        df_window = df[i - 14:i]

        RSI = get_rsi(df_window.Open.to_numpy(), df_window.Close.to_numpy())

        current_price = df_window.Open[13]

        if len(RSIs) > 0:
            last_rsi = RSIs[-1]

            # if last_rsi > 30 > RSI:
            if last_rsi < 30 and RSI < 30:
                if len(buys) == 0:
                    buys.append(current_price)
                    shares = int(default_buy / current_price)
                    num_of_shares.append(shares)
                    # print('buy', current_price)
                elif current_price < get_avg_share_price():
                    difference = (get_avg_share_price() - current_price) / current_price
                    new_buy = default_buy * (1 + 3 * difference)
                    shares = int(new_buy / current_price)

                    buys.append(current_price)
                    num_of_shares.append(shares)
                    # print('buy', current_price)

        RSIs.append(RSI)

    print('-------------- ' + share_name + ' ---------------')
    # print(buys, num_of_shares)
    print('number of buys', len(buys))
    print('avg buy price', get_avg_share_price())
    print('current price', df.Open[-1])
    print('capital gain', (df.Open[-1] - get_avg_share_price()) / get_avg_share_price())
    print('total value', get_avg_share_price() * sum(num_of_shares))

    if enable_graphs:
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.plot(df.Open[14:].to_numpy())
        ax2.plot(RSIs)
        ax2.axhline(y=70, color='r', linestyle='-')
        ax2.axhline(y=30, color='g', linestyle='-')

        plt.show()

    return (df.Open[-1] - get_avg_share_price())*sum(num_of_shares), get_avg_share_price()*sum(num_of_shares)


if __name__ == '__main__':
    # shares = ['SAMP', 'JKH', 'CTC', 'HNB', 'NDB', 'LLUB', 'EXPO', 'BRWN', 'DIAL', 'DIPD', 'HHL',
    #           'HAYL', 'RICH', 'RCL', 'LOLC', 'LFIN', 'MELS', 'TEEJ', 'VALI']
    #
    # # shares = ['DIAL']
    # gains_losses = []
    # capitals = []
    #
    # for share in shares:
    #     gain_loss, capital = evaluate(share, start_date='01/01/2010')
    #     gains_losses.append(gain_loss)
    #     capitals.append(capital)
    #
    # print('-------------------------------------------')
    # print('capital', sum(capitals))
    # print('Total gain', (sum(gains_losses) - sum(capitals))/sum(capitals))

    evaluate('TEEJ', start_date='01/01/2020', enable_graphs=True)