# Проверяем каждую минутную свечу. Ждем чтобы кол-во сделок за минуту было больше 1000.
# Ждем откатную свечуюКак только мы убеждаемся что она противоположная, то выставляем стоп-ордер по её хаю.
# Стоп лосс ниже лоэ
# Доработать открытие ордеров. Протестировать работоспособность
# Затеи прикрутить ловлю ножей(если мы продали по рынку и идет разворот(формируется и пробивается разворотная свеча))
# Мы это все отслеживаем но если у нас еще открыт ордер, то ждем его закрытия по стратегии, и только потом входим в противоход
import requests
import json
import time
import bitmex


def check_big_candle():
    # Проверяем изменение цены на лету за минуту, если больш 150 то открываем маркет по ходу движения
    print('вход в check_big_candle')
    min2=70
    s=1
    while True:
        time.sleep(10)
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
                if price_first - price>0:
                    orderQty = -100
                else:
                    orderQty = 100
                print('У нас нужное изменение цены, открываем маркет')
                with open("infa_onthe_orders.txt", "a") as file:
                    file.write(f"\ntime={timee}  price={price}  order-{orderQty}")
                return new_market_order(orderQty)

        print('s=', s)

# ---------------------------------------------------------------------------------------
# Модуль отвечает за манипуляции с ордерами

def new_market_order(orderQty):
    print(f'Мы вошли в функцию new_market_order сторона: {orderQty}')
    client = bitmex.bitmex(test=False, api_key='A8n4hPQLXfbnKy4CONZwQAPl',
                           api_secret='8aNSZRFE3ZzwbzMSyiqLXIzZTgeJUF6cUmXjrgTYW_1xjrfd')
    order_new_market = client.Order.Order_new(symbol='XRPUSD', orderQty=orderQty).result()
    ord_new_m_price = order_new_market[0]['price']
    orderID = order_new_market[0]['orderID']
    side = order_new_market[0]['side']
    timestamp = order_new_market[0]['timestamp']
    print (f'orderID: {orderID}')
    with open("market_order.txt", "a") as file:
        file.write(f"\norderID: {orderID}, price:{ord_new_m_price}, order:{orderQty},time:{timestamp}")
    with open("trades_history.txt", "a") as file:
        file.write(f"\nnew_market_order - time:{timestamp}, price:{ord_new_m_price}, side:{side},orderID: {orderID}")
    if orderQty > 0:
        ord_lim_price = ord_new_m_price + 0.0003 # +200 для биткоина
        orderQty = -1 # -100для биткоина
        stopPX = ord_new_m_price - 0.0003 # 100 для биткоина
        new_limit_order(orderQty, ord_lim_price)
        check_open_ord(orderQty, stopPX, ord_lim_price, orderID)
    else:
        ord_lim_price = ord_new_m_price - 0.0003
        orderQty = +1
        stopPX = ord_new_m_price + 0.0003 # 100 для биткоина
        new_limit_order(orderQty, ord_lim_price)
        check_open_ord(orderQty, stopPX, ord_lim_price, orderID)


def new_limit_order(orderQty, price):
    # открывает позицию (orderQty=+1)-на покупку. (orderQty=-1)-на продажу.записывает orderId в файл order_id
    print(f'Мы вошли в функцию new_limit_order сторона: {orderQty} цена: {price} ')
    client = bitmex.bitmex(test=False, api_key='A8n4hPQLXfbnKy4CONZwQAPl',
                           api_secret='8aNSZRFE3ZzwbzMSyiqLXIzZTgeJUF6cUmXjrgTYW_1xjrfd')
    order_new = client.Order.Order_new(symbol='XRPUSD', orderQty=orderQty, ordType='Limit', price=price).result()
    print('order_new - ',order_new)
    orderID = order_new[0]['orderID']
    side = order_new[0]['side']
    timestamp = order_new[0]['timestamp']
    price = order_new[0]['price']
    with open("limit_order.txt", "a") as file:
        file.write(f"\norderID: {orderID}, price:{price}, side:{side},time:{timestamp}")
    with open("trades_history.txt", "a") as file:
        file.write(f"\nnew_limit_order - time:{timestamp}, price:{price}, side:{side},orderID: {orderID}")
    print('лимитник выставлен  orderID: ',order_new[0]['orderID'])
    return


def check_open_ord(orderQty, stopPX, ord_lim_price, orderID):
    # функция слежения за открытым ордером, закрывать по стопу будем от сюда
    print('Мы вошли в функцию check_open_order')
    print(f'сторона: {orderQty} стоп-цена: {stopPX}\n'
          f'orderID {orderID} лимит-цена: {ord_lim_price}')
    while True:
        url = 'https://www.bitmex.com/api/v1/trade?symbol=XRPUSD&count=1&reverse=true'

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
    close_pos = client.Order.Order_closePosition(symbol='XRPUSD').result()
    print(f'type close_position = {type(close_pos)}')
    orderID = close_pos[0]['orderID']
    side = close_pos[0]['side']
    timestamp = close_pos[0]['timestamp']
    price = close_pos[0]['price']
    with open("trades_history.txt", "a") as file:
        file.write(f"\nclose_position -  time:{timestamp}, price:{price}, side:{side},orderID: {orderID}")



def close_all_position():
    # Закрывает все позиции.
    print('Мы в функции close_all_position')
    client = bitmex.bitmex(test=False, api_key='A8n4hPQLXfbnKy4CONZwQAPl',
                           api_secret='8aNSZRFE3ZzwbzMSyiqLXIzZTgeJUF6cUmXjrgTYW_1xjrfd')

    close_all = client.Order.Order_cancelAll().result()
    close_all= close_all[0]
    if len(close_all)>0:
        print(type(close_all))
        print(close_all)
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

if __name__=='__main__':
    close_all_position()
    #new_market_order(-1)
    #check_big_candle()
