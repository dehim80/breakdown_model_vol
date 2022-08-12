# Проверяем каждую минутную свечу. Ждем чтобы кол-во сделок за минуту было больше 1000.
# Ждем откатную свечуюКак только мы убеждаемся что она противоположная, то выставляем стоп-ордер по её хаю.
# Стоп лосс ниже ло
import requests
import json
import time
import bitmex
import websockets
import asyncio


async def main(): # функция подключатся к сокету и вынимает цену
    # url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    url = 'wss://ws.bitmex.com/realtime?subscribe=trade:XBTUSD'
    async with websockets.connect(url) as client:
        min2 = 70
        while True:
            try:
                data = json.loads(await client.recv())
                data = data['data']
                min1= time_now()[4:7]
                if min1 != min2:
                    price_first = round(data[0]['price'])
                    print('price_first:', price_first)

                min2 = min1
                for i in data:
                    price_ie = round(i['price'])
                    diff = abs(price_first - price_ie)
                    time_ie = i['timestamp']
                    print(f'time_ie: {time_ie}  price_ie: {price_ie}  diff: {diff}')
                    if abs(price_first - price_ie) > 150:
                        if price_first - price_ie > 0:
                            orderQty = -100
                        else:
                            orderQty = 100
                        print('У нас нужное изменение цены, открываем маркет')
                        with open("infa_onthe_orders.txt", "a") as file:
                            file.write(f"\ntime={time_ie}  price={price_ie}  order-{orderQty}")
                        return new_market_order(orderQty)

            except KeyError:
                print('кейеррор')





# ---------------------------------------------------------------------------------------
# Модуль отвечает за манипуляции с ордерами

def new_market_order(orderQty):
    print(f'Мы вошли в функцию new_market_order сторона: {orderQty}')
    client = bitmex.bitmex(test=False, api_key='A8n4hPQLXfbnKy4CONZwQAPl',
                           api_secret='8aNSZRFE3ZzwbzMSyiqLXIzZTgeJUF6cUmXjrgTYW_1xjrfd')
    order_new_market = client.Order.Order_new(symbol='XBTUSD', orderQty=orderQty).result()
    ord_new_m_price = order_new_market[0]['price']
    orderID = order_new_market[0]['orderID']
    side = order_new_market[0]['side']
    timestamp = order_new_market[0]['timestamp']
    print (f'price: {ord_new_m_price} orderID: {orderID}')
    with open("market_order.txt", "a") as file:
        file.write(f"\norderID: {orderID}, price:{ord_new_m_price}, order:{orderQty},time:{timestamp}")
    with open("trades_history.txt", "a") as file:
        file.write(f"\nnew_market_order - time:{timestamp}, price:{ord_new_m_price}, side:{side},orderID: {orderID}")
    if orderQty > 0:
        ord_lim_price = ord_new_m_price + 200 # +200 для биткоина
        orderQty = -100 # -100для биткоина
        stopPX = ord_new_m_price - 100 # 100 для биткоина
        new_limit_order(orderQty, ord_lim_price)
        check_open_ord(orderQty, stopPX, ord_lim_price, orderID)
    else:
        ord_lim_price = ord_new_m_price - 200
        orderQty = +100
        stopPX = ord_new_m_price + 100 # 100 для биткоина
        new_limit_order(orderQty, ord_lim_price)
        check_open_ord(orderQty, stopPX, ord_lim_price, orderID)


def new_limit_order(orderQty, price):
    # открывает позицию (orderQty=+1)-на покупку. (orderQty=-1)-на продажу.записывает orderId в файл order_id
    print(f'Мы вошли в функцию new_limit_order сторона: {orderQty} цена: {price} ')
    client = bitmex.bitmex(test=False, api_key='A8n4hPQLXfbnKy4CONZwQAPl',
                           api_secret='8aNSZRFE3ZzwbzMSyiqLXIzZTgeJUF6cUmXjrgTYW_1xjrfd')
    order_new = client.Order.Order_new(symbol='XBTUSD', orderQty=orderQty, ordType='Limit', price=price).result()
    orderID = order_new[0]['orderID']
    side = order_new[0]['side']
    timestamp = order_new[0]['timestamp']
    price = order_new[0]['price']
    with open("limit_order.txt", "a") as file:
        file.write(f"\norderID: {orderID}, price:{price}, side:{side},time:{timestamp}")
    with open("trades_history.txt", "a") as file:
        file.write(f"\nnew_limit_order   - time:{timestamp}, price:{price}, side:{side},orderID: {orderID}")
    print('лимитник выставлен  orderID: ',order_new[0]['orderID'])
    return


def check_open_ord(orderQty, stopPX, ord_lim_price, orderID):
    # функция слежения за открытым ордером, закрывать по стопу будем от сюда
    print('Мы вошли в функцию check_open_order')
    print(f'сторона: {orderQty} стоп-цена: {stopPX}\n'
          f'orderID {orderID} лимит-цена: {ord_lim_price}')
    while True:
        url = 'https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&count=1&reverse=true'

        resp = requests.get(url).text
        data = json.loads(resp)
        data1 = (data[0]['price'])
        time.sleep(2)
        if orderQty > 0:  # Если открыта продажа то
            if data1 >= stopPX or data1 <= ord_lim_price:
                print('Вариант 1')
                close_all_position()
                close_position() #100 для биткоина
                return

        else:  # Если покупка то
            if data1 <= stopPX or data1 >= ord_lim_price:
                print('Вариант 2')
                close_all_position()
                close_position() #-100 для биткоина
                return


def close_position():
    print(f'Мы вошли в функцию close_position')
    client = bitmex.bitmex(test=False, api_key='A8n4hPQLXfbnKy4CONZwQAPl',
                               api_secret='8aNSZRFE3ZzwbzMSyiqLXIzZTgeJUF6cUmXjrgTYW_1xjrfd')
    close_pos = client.Order.Order_closePosition(symbol='XBTUSD').result()
    print(f'type close_position = {type(close_pos)}')
    orderID = close_pos[0]['orderID']
    side = close_pos[0]['side']
    timestamp = close_pos[0]['timestamp']
    price = close_pos[0]['price']
    with open("trades_history.txt", "a") as file:
        file.write(f"\nclose_position   -  time:{timestamp}, price:{price}, side:{side},orderID: {orderID}")


def close_all_position():
    # Закрывает все позиции.
    print('Мы в функции close_all_position')
    client = bitmex.bitmex(test=False, api_key='A8n4hPQLXfbnKy4CONZwQAPl',
                           api_secret='8aNSZRFE3ZzwbzMSyiqLXIzZTgeJUF6cUmXjrgTYW_1xjrfd')

    close_all = client.Order.Order_cancelAll().result()
    close_all= close_all[0]
    if len(close_all)>0:
        timestamp = close_all[0]['timestamp']
        orderID = close_all[0]['orderID']
        side = close_all[0]['side']
        price = close_all[0]['price']
        with open("trades_history.txt", "a") as file:
            file.write(f"\nclose_all_position- time:{timestamp}, price:{price}, side:{side},orderID: {orderID}")
        print('Все ордера закрыты')

#-------------------------------------------------------------------------------------------------------
#      модуль отвечает за время

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

def time_hist():
    date_m = time.gmtime().tm_mon
    date_d = time.gmtime().tm_mday
    time_h = time.gmtime().tm_hour
    time_min = time.gmtime().tm_min
    time_s = time.gmtime().tm_sec
    return f'{date_m}-{date_d}  {time_h}:{time_min}:{time_s}'

def date_now():
    date_y = time.gmtime().tm_year
    date_m = time.gmtime().tm_mon
    date_d = time.gmtime().tm_mday
    return(f'{date_y}-{date_m}-{date_d}')

#-------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
