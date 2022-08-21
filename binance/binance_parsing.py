import requests

import time


def write_in_exel():

    print('Мы в функции write_in_exel')
    resp_trade = requests.get('https://testnet.binancefuture.com/fapi/v1/trades?symbol=BTCUSDT') #2
    resp_trade_json = resp_trade.json()
    print(resp_trade_json)


if __name__=='__main__':
    write_in_exel()