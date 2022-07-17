import json, time
import requests
from time_modul import time_mod_midnight, time_now, time_mod

def main():
    create_channel()


def create_channel():
    # Каждые 5 минут сканирует предыдущие 4 часа на наличие узкого коридора. Начиная с 4:30.Возвращает границы
    # С 00 до 4-30 перерыв в виду малой активности рынкаtime_mod_midnight()
    time_mod_midnight()
    url = (f'https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBTUSD'
           f'&columns=high%2C%20low&count=48&reverse=true&endTime={time_now()}')
    resp = requests.get(url).text
    data = json.loads(resp)
    high_elts = []
    low_elts = []
    for h in range(48):
        high_elts.append(data[h]['high'])
        low_elts.append(data[h]['low'])
    high_elts.sort(reverse=True)
    low_elts.sort()
    print(f'high= {high_elts[0]}   low= {low_elts[0]}')
    diff = high_elts[0] - low_elts[0]
    high_el = high_elts[0]
    low_el = low_elts[0]
    if diff > 200:
        time_mod()
    else:
        return check_activ_ord(high_el, low_el)


def check_activ_ord(high_el, low_el):
    # Следим за ценой и открываем ордер
    k = 1
    while True:
        url = 'https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&count=1&reverse=true'

        resp = requests.get(url).text
        data = json.loads(resp)
        data1 = (data[0]['price'])
        print(k,data1)
        time.sleep(2)


if __name__ == '__main__':
    main()