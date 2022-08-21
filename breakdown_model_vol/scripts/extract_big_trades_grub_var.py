# Записывает в файл весь месяц поминутно- трейды и кол-во сделок. если за минуту цена прошла > 150dol
# дальнейшие вычисления строятся на хае и лоу следующих свечей.Поэтому это грубый вариант
# сделать так чтобы в минуте в которой Ю150 дол. как будто открывалась сделка по ходу движения
# и записывался в файл результат сделки, чтобы собрать статистику за пол года.Сделать с этиими же минутами ловлю ножей

import json
import time
import pandas as pd
import requests

def big_size(date, spisok, month):
    print(f'Мы в функции big_size.  date={date}')

    resp_trade = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&columns=open%2C%20close%2C%20high%2C%20low%2C%20trades%2C%20volume&'
        f'count=1000&start=0&reverse=false&startTime=2022-{month}-{date}%2000%3A01').text

    data = json.loads(resp_trade)
    for i in range(1000):

        cl_candle = data[i]['close']
        op_candle = data[i]['open']
        low_candle = data[i]['low']
        hi_candle = data[i]['high']
        timee = data[i]['timestamp']
        if op_candle - cl_candle > 0 and op_candle - low_candle > 150: # Если красная свеча
            open_price = op_candle-150
            spisok.append({'type':'sell_market','result':0,'time':timee, 'price': open_price})
            con = i+1
            count = 1000
            start = 0
            sell_trade(open_price, timee, month, date, count, start, con, spisok)
        if op_candle - cl_candle < 0 and hi_candle - op_candle > 150: # Если зеленая свеча
            open_price = op_candle + 150
            spisok.append({'type':'buy_market','result':0,'time':timee, 'price': open_price})
            con = i+1
            count = 1000
            start = 0
            buy_trade(open_price, timee, month, date, count, start, con, spisok)



    resp_trade2 = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&columns=open%2C%20close%2C%20high%2C%20low%2C%20trades%2C%20volume&'
        f'count=438&start=1001&reverse=false&startTime=2022-{month}-{date}%2000%3A01').text
    data = json.loads(resp_trade2)
    for i in range(438):
        cl_candle = data[i]['close']
        op_candle = data[i]['open']
        low_candle = data[i]['low']
        hi_candle = data[i]['high']
        timee = data[i]['timestamp']
        if op_candle - cl_candle > 0 and op_candle - low_candle > 150:  # Если красная свеча
            open_price = op_candle - 150
            spisok.append({'type':'sell_market','result':0,'time':timee, 'price': open_price})
            con = i+1
            count = 438
            start = 1001
            sell_trade(open_price,timee, month, date, count, start, con, spisok)
        if op_candle - cl_candle < 0 and hi_candle - op_candle > 150:  # Если зеленая свеча
            open_price = op_candle + 150
            spisok.append({'type':'buy_market','result':0,'time':timee, 'price': open_price})
            con = i+1
            count = 438
            start = 1001
            buy_trade(open_price, timee, month, date, count, start, con, spisok)


    # df = pd.DataFrame(spisok)
    # df.to_excel(f'./hist2022-{month}-{date}-all-day.xlsx', index=False)


def sell_trade(open_price, timee, month, date, count, start, con,spisok):
    time.sleep(2)
    print(f'Мы в sell_trade()  open_price: {open_price} time: {timee}')
    resp_trade2 = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&columns=open%2C%20close%2C%20high%2C%20low%2C%20trades%2C%20volume&'
        f'count={count}&start={start}&reverse=false&startTime=2022-{month}-{date}%2000%3A01').text
    data = json.loads(resp_trade2)
    for i in range(con, count):
        low_candle = data[i]['low']
        hi_candle = data[i]['high']
        time_data = data[i]['timestamp']
        for u in range(100, 0, -100):
            if hi_candle - open_price >= 100:
                spisok.append({'type': 'stop_loss', 'result': -100, 'time': time_data, 'price': hi_candle})
                return
            if open_price - low_candle >= u:
                spisok.append({'type': 'take_profit', 'result': u, 'time': time_data, 'price': hi_candle})
                return


def buy_trade(open_price, timee, month, date, count, start, con,spisok):
    time.sleep(2)
    print(f'Мы в buy_trade()  open_price: {open_price} time: {timee}')
    resp_trade2 = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&columns=open%2C%20close%2C%20high%2C%20low%2C%20trades%2C%20volume&'
        f'count={count}&start={start}&reverse=false&startTime=2022-{month}-{date}%2000%3A01').text
    data = json.loads(resp_trade2)
    for i in range(con, count):
        low_candle = data[i]['low']
        hi_candle = data[i]['high']
        time_data = data[i]['timestamp']
        for u in range(100, 0, -100):
            if open_price - low_candle >= 100:
                spisok.append({'type': 'stop_loss', 'result': -100, 'time': time_data, 'price': low_candle})
                return
            if hi_candle - open_price >= u:
                spisok.append({'type': 'take_profit', 'result': u, 'time': time_data, 'price': low_candle})
                return
    return


def write_in_exel(hourr, minn, month, date):
    time.sleep(1)
    minn = int(minn)
    minn-=1
    print('Мы в функции write_in_exel')
    resp_trade = requests.get('https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&columns=side%2C%20size%2C%20price&count=1000&'
                              f'start=1&reverse=false&startTime=2022-{month}-{date}%20{hourr}%3A{minn}') #2
    resp_trade_json = resp_trade.json()
    df = pd.DataFrame(resp_trade_json)
    df.to_excel(f'./hist2022-{month}-{date}-one-min-{hourr}-{minn}.xlsx', index=False) #2
    time.sleep(1)
    return



def counter(spisok,month):
    for date in range(1,31):
        big_size(date,spisok,month)
    return


if __name__ == '__main__':
    spisok = []
    month = 6
    counter(spisok,month)
    df = pd.DataFrame(spisok)
    df.to_excel(f'./hist2022-{month}-trade_history.xlsx', index=False)
    print('end program')
