import json
import time

import pandas as pd
import requests


def big_size(date):  # Записывает в файл весь месяц поминутно- трейды и кол-во сделок. если за минуту сделок>1000
    print(f'Мы в функции big_size.  date={date}')  # то записывает отдельный ексель с этой минутой по еденичным сделкам
    month = '08'
    spisok = []
    resp_trade = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&columns=trades%2Cvolume&'
        f'count=1000&start=0&reverse=false&startTime=2022-{month}-{date}%2000%3A01').text
    print(type(resp_trade))
    data = json.loads(resp_trade)
    for i in range(1000):
        amount_trades = data[i]['trades']
        if amount_trades > 1000:
            print('amount_trades', amount_trades)
            print(data[i]['timestamp'])
            hourr = data[i]['timestamp'][11:13]
            minn = data[i]['timestamp'][14:16]
            write_in_exel(hourr, minn, month, date)
            print(hourr, minn)
        spisok.append(data[i])

    resp_trade2 = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&columns=trades%2Cvolume&'
        f'count=438&start=1001&reverse=false&startTime=2022-{month}-{date}%2000%3A01').text
    data = json.loads(resp_trade2)
    for i in range(438):
        amount_trades = data[i]['trades']
        if amount_trades > 1000:
            print(data[i]['timestamp'])
            hourr = data[i]['timestamp'][11:13]
            minn = data[i]['timestamp'][14:16]
            write_in_exel(hourr, minn, month, date)
            print(hourr, minn)
        spisok.append(data[i])

    df = pd.DataFrame(spisok)
    df.to_excel(f'./hist2022-{month}-{date}-all-day.xlsx', index=False)


def write_in_exel(hourr, minn, month, date):
    time.sleep(1)
    minn = int(minn)
    minn -= 1
    print('Мы в функции write_in_exel')
    resp_trade = requests.get(
        'https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&columns=side%2C%20size%2C%20price&count=1000&'
        f'start=1&reverse=false&startTime=2022-{month}-{date}%20{hourr}%3A{minn}')  # 2
    resp_trade_json = resp_trade.json()
    df = pd.DataFrame(resp_trade_json)
    df.to_excel(f'./hist2022-{month}-{date}-one-min-{hourr}-{minn}.xlsx', index=False)  # 2
    time.sleep(1)
    return


def counter():
    for i in range(1, 13):
        big_size(i)
    return


if __name__ == '__main__':
    counter()
    print('end program')
