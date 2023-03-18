# Alex Klimov ордера Binance Futures на Python
# Записывает в файл глубинный стакан на фьючерсах.Нужно доделать запись стакана на споте.Пока не вижу смысла
# Хотел зацепиться за большой обьем и отскок от него или разбор его,  но разбор происходитт очень быстро и не успеть...

import time
import pandas as pd
import datetime
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

api_key = '3VzwQ1U53lVLtmY05H2yyZPQxf0u88Usw94RjMu0VlPDq9IMydYSKDPB75caqsjZ'
api_secret = 'fABGUHH8d4TlHpBZ1ORu58XPC97y5rbudhtT7CuhdKzGUrLk3pJyeF8ewkcmnIQE'


def deep_depth():
    old_sec = 0
    print('1old sec=', old_sec)
    llist = []
    while True:
        client = Client(api_key=api_key, api_secret=api_secret)
        data_servertime = client.futures_time()
        data_unixtime = data_servertime['serverTime']

        depth_spot = client.get_order_book(symbol='BTCUSDT')
        depth_futures = client.futures_order_book(symbol='BTCUSDT')


        bids_futures = (depth_futures['bids'])
        asks_futures = (depth_futures['asks'])
        print('2old sec=', old_sec)
        for el in asks_futures:
            ask_vol = float(el[1])
            ask_price = float(el[0])
            if ask_vol > 10:
                data_time = conv_un_time(data_unixtime)
                llist.append({'time': data_time, 'ask_price': ask_price, 'quantity': ask_vol})
        for el in bids_futures:
            bid_vol = float(el[1])
            bid_price = float(el[0])
            if bid_vol > 10:
                data_time = conv_un_time(data_unixtime)
                print(f'time:{data_time} price:{bid_price}, quantity:{bid_vol}')
                llist.append({'time': data_time, 'bid_price': bid_price, 'quantity': bid_vol})

        bids_spot = (depth_spot['bids']) # Достаем спротовые биды
        asks_spot = (depth_spot['asks']) #
        print(bids_spot)
        print(asks_spot)
        # Дальше не законченный код. Нужно поставить проверку на большой обьем и добавление в лист
        # по анологии с фьючерсами
        print('3old sec=', old_sec)
        if time_sec() == 0 or time_sec() < old_sec:
            if len(llist) > 20:
                df = pd.DataFrame(llist)
                df.to_excel(f'depth{time_now()}.xlsx', index=False)
                llist = []
                print('4old sec=', old_sec)
        old_sec = time_sec()
        print('5old sec=', old_sec)
        time.sleep(20)


def conv_un_time(millis):
    unix_time = millis / 1000
    dt = datetime.datetime.utcfromtimestamp(unix_time)
    gmt3_tz = datetime.timezone(datetime.timedelta(hours=3))
    dt = dt.replace(tzinfo=datetime.timezone.utc).astimezone(gmt3_tz)
    return (dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])


def time_now():
    loc_sec = time.gmtime().tm_sec
    loc_hour = time.localtime().tm_hour
    loc_min_plus_one = time.gmtime().tm_min
    loc_min = loc_min_plus_one - 1
    loc_date = time.gmtime().tm_mday
    loc_month = time.gmtime().tm_mon
    loc_year = time.gmtime().tm_year
    return f'{loc_year}-{loc_month}-{loc_date} {loc_hour}-{loc_min}-{loc_sec}'


def time_sec():
    loc_sec = time.gmtime().tm_sec
    return loc_sec


if __name__ == '__main__':
    deep_depth()
