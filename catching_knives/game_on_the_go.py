# Проверяем каждую минутную свечу. Ждем чтобы кол-во сделок за минуту было больше 1000.
# Ждем откатную свечуюКак только мы убеждаемся что она противоположная, то выставляем стоп-ордер по её хаю.
# Стоп лосс ниже лоэ
import requests
import json
import time
import pandas as pd


def check_big_candle():
    # Проверяем изменение цены на лету за минуту, если больше 150 то открываем маркет по ходу движения
    print('вход в check_big_candle')
    min2=70
    s=1
    while True:
        time.sleep(4)
        min1=time_now()[5:7]
        if min2!=min1:
            s=1

        url = f'https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&columns=price&count=1000&start={s}&reverse=false&' \
              f'startTime={date_now()}%20{time_now()}'

        resp = requests.get(url).text
        data = json.loads(resp)
        lenght = len(data)
        if s==1 and lenght != 0:
            price_first = data[0]['price']
            print('price_first=', price_first)
        s = s+lenght
        print(time_now())
        print('len data=', lenght)
        min2 = time_now()[5:7]

        for i in range(lenght):
            price = data[i]['price']
            timee= data[i]['timestamp'][11:19]
            print(f'time={timee}  price={price}')
            if abs(price_first-price)>150:
                print('У нас нужное изменение цены, открываем маркет')
                break

        print('s=', s)







#-------------------------------------------------------------------------------------------------------
# модуль отвечает за время
def time_mod():
    print('Ждем минуту ')
    time.sleep(1)
    while True:
        local_time = time.localtime().tm_sec
        time.sleep(0.5)
        if local_time == 15:
            return


def time_now():
    time_h = time.gmtime().tm_hour
    time_m = time.gmtime().tm_min
    return f'{time_h}%3A{time_m}'

def date_now():
    date_y = time.gmtime().tm_year
    date_m = time.gmtime().tm_mon
    date_d = time.gmtime().tm_mday
    return(f'{date_y}-{date_m}-{date_d}')
#-------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    check_big_candle()