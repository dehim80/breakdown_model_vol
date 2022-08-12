import requests
import json
import time
import bitmex
import websockets
import asyncio
# функция подключатся к сокету и вынимает цену

async def main():
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
                    if abs(price_first - price_ie) > 10:
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


def time_now():
    time_h = time.gmtime().tm_hour
    time_m = time.gmtime().tm_min
    return f'{time_h}%3A{time_m}'


def new_market_order(orderQty):
    print(f'Мы открыли ордер. Сторона {orderQty}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print('stop program')