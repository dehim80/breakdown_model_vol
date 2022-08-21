import requests, time
from bitmex_websocket import BitMEXWebsocket
import socket


def main():
    endpoint='wss://ws.bitmex.com/realtime'


    sock = socket.socket()
    sock.connect((endpoint,443))
    sock.send({"op": "subscribe", "args": ["orderBookL2_25:XBTUSD"]})

    data = sock.recv(1024)
    print(data)
    sock.close()





def time_now():
    time_h = time.gmtime().tm_hour
    time_m = time.gmtime().tm_min
    return f'{time_h}%3A{time_m}'


def new_market_order(orderQty):
    print(f'Мы открыли ордер. Сторона {orderQty}')


if __name__ == '__main__':
    main()