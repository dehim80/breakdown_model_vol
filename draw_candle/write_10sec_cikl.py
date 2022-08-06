import time

import pandas as pd
import requests


def write_10sec(min, master_list): # разбивает минутку на 10 секундные свечи
    print(f'Мы в функции write_10sec min= {min}')
    date = '2022-07-28'
    hour = '20'
    min2 = min+1
    resp = requests.get('https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&columns=size%2C%20price&count=1000&reverse=false&'
                        f'startTime={date}%20{hour}%3A{min}&endTime={date}%20{hour}%3A{min2}') #1

    resp_json = resp.json()

    listt1 = []
    listt2 = []
    listt3 = []
    listt4 = []
    listt5 = []
    listt6 = []

    # master_list=[]
    for i in range(len(resp_json)):
        sec = int((resp_json[i]['timestamp'])[17:19])
        if sec >= 0 and sec <10:
            listt1.append(resp_json[i]['price'])
        elif sec>=10 and sec <20:
            listt2.append(resp_json[i]['price'])
        elif sec>=20 and sec <30:
            listt3.append(resp_json[i]['price'])
        elif sec>=30 and sec <40:
            listt4.append(resp_json[i]['price'])
        elif sec>=40 and sec <50:
            listt5.append(resp_json[i]['price'])
        elif sec>=50 and sec <60:
            listt6.append(resp_json[i]['price'])

    if len(listt1) > 0:
        open = listt1[0]
        close = listt1[-1]
        listt1.sort()
        low = listt1[0]
        high = listt1[-1]
        print(f'open {open} close-{close} low-{low} high-{high}')
        dictt1={'time':f'{hour}:{min}:00','open': open, 'high': high, 'low': low, 'close': close}
        master_list.append(dictt1)

    if len(listt2)>0:
        open = listt2[0]
        close = listt2[-1]
        listt2.sort()
        low = listt2[0]
        high = listt2[-1]
        print(f'open {open} close-{close} low-{low} high-{high}')
        dictt2 = {'time':f'{hour}:{min}:10','open': open, 'high': high, 'low': low, 'close': close}
        master_list.append(dictt2)

    if len(listt3) > 0:
        open = listt3[0]
        close = listt3[-1]
        listt2.sort()
        low = listt3[0]
        high = listt3[-1]
        print(f'open {open} close-{close} low-{low} high-{high}')
        dictt3 = {'time': f'{hour}:{min}:20', 'open': open, 'high': high, 'low': low, 'close': close}
        master_list.append(dictt3)

    if len(listt4) > 0:
        open = listt4[0]
        close = listt4[-1]
        listt2.sort()
        low = listt4[0]
        high = listt4[-1]
        print(f'open {open} close-{close} low-{low} high-{high}')
        dictt4 = {'time': f'{hour}:{min}:30', 'open': open, 'high': high, 'low': low, 'close': close}
        master_list.append(dictt4)

    if len(listt5) > 0:
        open = listt5[0]
        close = listt5[-1]
        listt2.sort()
        low = listt5[0]
        high = listt5[-1]
        print(f'open {open} close-{close} low-{low} high-{high}')
        dictt5 = {'time': f'{hour}:{min}:40', 'open': open, 'high': high, 'low': low, 'close': close}
        master_list.append(dictt5)

    if len(listt6) > 0:
        open = listt6[0]
        close = listt6[-1]
        listt2.sort()
        low = listt6[0]
        high = listt6[-1]
        print(f'open {open} close-{close} low-{low} high-{high}')
        dictt6 = {'time': f'{hour}:{min}:50', 'open': open, 'high': high, 'low': low, 'close': close}
        master_list.append(dictt6)


def counter(master_list):
    for min in range(20,59):
        time.sleep(2)
        write_10sec(min, master_list)
    df = pd.DataFrame(master_list)
    df.to_csv(f'./hist2022-07-28-(20-20-58)sec.csv', index=False)  # 1
    #df.to_excel(f'./hist2022-07-30-(18-28-39)sec.xlsx', index=False)
    df.to_excel()


if __name__ == '__main__':
    master_list = []
    counter(master_list)