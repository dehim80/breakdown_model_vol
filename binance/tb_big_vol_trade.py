import websockets
import asyncio
import json
import time
import bitmex
import datetime
import requests


# Задаю уровень вручную.Подключаемся к сокету, мониторим цену. Как только цена пробила уровень и обьем больше 1К,открываем
# позицию.Закрываем сокет и дальше request-ом открываем позицию, ставим стопы.

async def main(level): # Функция подключается к сокету и мониторит цену и обьем.Как только цена выходит за level и
    retries = 0        # обьем в текущей свече > 2000 то переходим к функции открытия ордера
    sum_of_vol = 0
    old_sec = 0
    counter = -1 # Счетчик. Первый заход делаем -1 чтобы оприделить уровень выше или ниже текущей цены
    url = "wss://fstream.binance.com/ws/btcusdt@aggTrade" # Если один параметр
    print('main_function')
    while True:
        try:
            async with websockets.connect(url) as client:
                print('Начало скрипта')
                while True:
                    data = json.loads(await client.recv())
                    data_price = float(data['p'])
                    data_quan = float(data['q']) # каждый отдельный обьем сделки
                    sum_of_vol += data_quan
                    if counter == 1: # Оприделяем первую цену в свече
                        first_price = data_price
                        print(f'level = {level} price = {first_price}')
                    if counter == -1: # оприделяем level выше или ниже текущей цены
                        if data_price < level:
                            location_level = 1
                        else:
                            location_level = -1
                        print(f'Оприделили location_leve = {location_level}')
                    if location_level == 1 and sum_of_vol > 1000 and data_price > level: # 1000 Если level выше текущей цены
                        print('open buy market order')
                        orderQty = location_level*100
                        client.close()
                        print('Закрыли сокет')
                        new_market_order(orderQty)
                        break
                        # закрываем сокет и переходим к открытию ордера и выставления стоп лосса и тейк профита
                    if location_level == -1 and sum_of_vol > 1000 and data_price < level: # 1000 Если level ниже текущей цены
                        print('open buy market order')
                        orderQty = location_level*100
                        client.close()
                        print('Закрыли сокет')
                        new_market_order(orderQty) # asyncio.create_task
                        break
                    if time_sec() == 0 and time_sec() < old_sec: # если началась новая минута, то сбрасываем счетчик
                        print('time_sec() == 0   Новая минута сбрасываем счетчики')
                        print('max_vol=', sum_of_vol)
                        counter = 0
                        sum_of_vol = 0
                    counter += 1
                    old_sec = time_sec()
        except websockets.exceptions.ConnectionClosedError:
            print("Ошибка: соединение было закрыто без отправки фрейма закрытия. Переподключение...")
            await client.close()
            print('11111')
            # ждем несколько секунд перед повторной попыткой подключения
            await asyncio.sleep(20)
            print('2222222')
            retries += 1
        break


def new_market_order(orderQty):
    print(f'Мы вошли в функцию new_market_order сторона: {orderQty}')
    client = bitmex.bitmex(test=False, api_key='wAPUL0s094kCwzErt17KiFBD',
                           api_secret='qe9jpgUf_EVTNIvtc6PNMHzQl8sssJlW5C3rRefWFWcMhG6Y')
    order_new_market = client.Order.Order_new(symbol='XBTUSD', orderQty=orderQty).result()
    ord_new_m_price = order_new_market[0]['price']
    orderID = order_new_market[0]['orderID']
    print(f'orderID: {orderID}')
    mess = f'open market order pos:{orderQty} price:{ord_new_m_price}'
    print(mess)
    send_message(mess)
    stop_order(orderQty, ord_new_m_price) # Выставляем стоп-ордер
    limit_order(orderQty, ord_new_m_price) # Выставляем лимитник на прибыль
    pos() # Чекаем позицию, если закрылась то
    close_all_position() # отменяем все ордера


def stop_order(orderQty, ord_new_m_price):
    print('Зашли в функцию стопордер')
    if orderQty>0:
        stop_price = ord_new_m_price - 50
    else:
        stop_price = ord_new_m_price + 50
    mess = f'сторона {orderQty} цена выставления стопа {stop_price}'
    print(mess)
    send_message(mess)
    orderQty = orderQty * (-1)
    client = bitmex.bitmex(test=False, api_key='wAPUL0s094kCwzErt17KiFBD',
                           api_secret='qe9jpgUf_EVTNIvtc6PNMHzQl8sssJlW5C3rRefWFWcMhG6Y')
    stop_order = client.Order.Order_new(symbol='XBTUSD', orderQty=orderQty, ordType='Stop', stopPx=stop_price).result()
    print('stop_order', stop_order)
    return stop_price
    

def limit_order(orderQty, ord_new_m_price):
    print('Зашли в функцию лимитордер')
    if orderQty>0:
        limit_price = ord_new_m_price + 500
    else:
        limit_price = ord_new_m_price - 500
    mess = f'сторона {orderQty} цена выставления лимита {limit_price}'
    print(mess)
    send_message(mess)
    orderQty = orderQty * (-1)
    client = bitmex.bitmex(test=False, api_key='wAPUL0s094kCwzErt17KiFBD',
                           api_secret='qe9jpgUf_EVTNIvtc6PNMHzQl8sssJlW5C3rRefWFWcMhG6Y')
    limit_order = client.Order.Order_new(symbol='XBTUSD', orderQty=orderQty, ordType='Limit', price=limit_price).result()
    print('limit_order', limit_order)
    return limit_price


def pos():
    client = bitmex.bitmex(test=False, api_key='wAPUL0s094kCwzErt17KiFBD',
                           api_secret='qe9jpgUf_EVTNIvtc6PNMHzQl8sssJlW5C3rRefWFWcMhG6Y')
    while True:
        pos = client.Position.Position_get().result()
        position = pos[0]
        for el in position:
            if el['symbol'] =='XBTUSD':
                if el['currentQty'] == 0:
                    print('Нет открытой позиции по XRPUSD')
                    realisedPnl = el['realisedPnl']
                    mess = f'реализованный Pnl:{realisedPnl}'
                    send_message(mess)
                    return
                if el['currentQty'] != 0:
                    liverage = el['leverage']
                    realisedPnl = el['realisedPnl']
                    unrealisedPnl = el['unrealisedPnl']
                    EntryPrice = el['avgEntryPrice']
                    print (f'открыта позиция по XRPUSD. цена входа {EntryPrice} leverage {liverage} ')
                    print(f'реализованный Pnl {realisedPnl} нереализованный Pnl {unrealisedPnl}')
        time.sleep(10)


def close_all_position():
    # Закрывает все позиции.
    print('Мы в функции close_all_position')
    client = bitmex.bitmex(test=False, api_key='wAPUL0s094kCwzErt17KiFBD',
                           api_secret='qe9jpgUf_EVTNIvtc6PNMHzQl8sssJlW5C3rRefWFWcMhG6Y')

    client.Order.Order_cancelAll().result()
    print('Все ордера закрыты')


def time_now():
    loc_sec = time.gmtime().tm_sec
    loc_hour = time.localtime().tm_hour
    loc_min_plus_one= time.gmtime().tm_min
    loc_min = loc_min_plus_one -1
    loc_date = time.gmtime().tm_mday
    loc_month = time.gmtime().tm_mon
    loc_year = time.gmtime().tm_year
    return f'{loc_year}-{loc_month}-{loc_date} {loc_hour}-{loc_min}-{loc_sec}'


def conv_un_time(millis):
    unix_time = millis / 1000
    dt = datetime.datetime.utcfromtimestamp(unix_time)
    gmt3_tz = datetime.timezone(datetime.timedelta(hours=3))
    dt = dt.replace(tzinfo=datetime.timezone.utc).astimezone(gmt3_tz)
    return (dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])


def time_sec():
    loc_sec = time.gmtime().tm_sec
    return loc_sec


def send_message(mess):
    bot = '5896626762:AAHGpDL53QbVY9uwareE3rpiYUKy4ouhAQY'
    chat_id = 739957796
    url = f'https://api.telegram.org/bot{bot}/sendMessage'
    params = {'chat_id': chat_id, 'text': mess}
    resp = requests.post(url, data=params)
    print('resp', resp)


if __name__ == '__main__':
    print('if name == main')
    level = 27400
    asyncio.get_event_loop().run_until_complete(main(level))
    asyncio.get_event_loop().stop()
