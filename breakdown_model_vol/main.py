# аналог зигзага выдает точки минимума и максимума
import time
import pandas as pd
import requests


def high_low_point(): # запрос каждую минуту.
    print('Мы в функции high_low_point')

    gen_list = []
    depth = 70
    resp = requests.get('https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&'
                    f'columns=open%2C%20close%2C%20high%2C%20low%2C%20trades%2C%20volume&count=120&start=1&reverse=false'
                    f'&startTime=2022-08-15%2004%3A00')

    resp_json = resp.json()
    low = resp_json[0]['low']
    high = resp_json[0]['high']



    for i in range(1,120):
        print('1 i=', i)
        if high-resp_json[i]['low'] > depth:
            i= i+1
            low = resp_json[i]['low']
            time_l = resp_json[i]['timestamp'][12:16]
            time = resp_json[0]['timestamp'][12:16]
            print('low= ',low)
            gen_list.append({time:high})
            print ('high_list.append(high)', high)
            #print('цена идет вниз')
            count = i
            lower(count,low,time_l, gen_list,depth, resp_json)

        if resp_json[i]['high'] - low > depth:
            i = i + 1
            high = resp_json[i]['high']
            time = resp_json[0]['timestamp'][12:16]
            time_h = resp_json[i]['timestamp'][12:16]
            gen_list.append({time:low})

            #print('цена идет вверх')
            count = i
            higher(count,high,time_h, gen_list,depth, resp_json)



def lower(count,low,time_l, gen_list,depth, resp_json):
    if count == 119: return
    #print('мы в lower')
    #print(f'count:{count} low: {low} gen_l: {gen_list}')
    for i in range(count,120):
        if i == 119:
            #print('из lower переходим в fin')
            create_model(gen_list)

        if resp_json[i]['low']< low:
            low = resp_json[i]['low']
            time_l = resp_json[i]['timestamp'][12:16]
            i+=1
        if resp_json[i]['high']-low>depth:
            #print(f'добавляем low: {low}')
            gen_list.append({time_l:low})
            high = resp_json[i]['high']
            time_h = resp_json[i]['timestamp'][12:16]
            count = i+1
            higher(count, high,time_h,gen_list, depth, resp_json)


def higher(count,high,time_h,gen_list, depth, resp_json):
    #print('мы в higher')
    #print(f'count:{count} high: {high} gen_l: {gen_list}')
    for i in range(count, 120):
        if i == 119:
            #print('из higher переходим в fin')
            create_model(gen_list)
        if resp_json[i]['high'] > high:
            high = resp_json[i]['high']
            time_h = resp_json[i]['timestamp'][12:16]
            i+=1
        if high - resp_json[i]['low'] > depth:
            #print(f'добавляем high: {high}')
            gen_list.append({time_h:high})
            low = resp_json[i]['low']
            time_l = resp_json[i]['timestamp'][12:16]
            count = i+1
            lower(count, low,time_l, gen_list, depth, resp_json)






        # df = pd.DataFrame(resp_json)
        # df.to_excel('./hist130709-00.xlsx', index=False)


def create_model(gen_list):
    print('мы в create_model')
    for element in gen_list:
        print(element)
    print('end program')
    quit()

def time_mod():
    # Функция ждет, пока обнулится минута.
    while True:
        loc_sec = time.localtime().tm_sec
        time.sleep(0.5)
        if loc_sec == 0:
            break


def time_now():
    time_mod()
    time.sleep(5)
    time_h = time.gmtime().tm_hour
    time_m = time.gmtime().tm_min
    return f'{time_h}%3A{time_m}'


if __name__ == '__main__':
    high_low_point()
    print('Finnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')

