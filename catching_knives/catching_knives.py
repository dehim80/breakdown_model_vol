# Проверяем каждую минутную свечу. Ждем чтобы кол-во сделок за минуту было больше 1000.
# Ждем откатную свечуюКак только мы убеждаемся что она противоположная, то выставляем стоп-ордер по её хаю.
# Стоп лосс ниже лоэ
import requests
import json
import time
import pandas as pd


def check_trades():
    # Проверяем кол-во трейдов, если он больше заданного, то переходим дальше
    print('вход в чек трейдс')
    i = 1
    while True:
        url = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=1&reverse=true'
        resp = requests.get(url).text
        data = json.loads(resp)
        data1 = data[0]
        vol = data1['trades']
        print(f'проход № {i}  Количество сделок: {vol} время:', time_now())
        i += 1
        if vol < 1000:  # 1000 нужный параметр
            print('Маленькое кол-во сделок')
            time_mod()
        else:
            print('У нас нужный объём, выполняем проверку на отклонение за последние 10 свечей')
            return deviation_price()


def deviation_price():
    # проверка на отклонение за последние 10 свечей
    url2 = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=10&reverse=true'
    resp2 = requests.get(url2).text
    resp2_json = json.loads(resp2)
    resp_close_now = resp2_json[0]['close']
    resp_close_ten = resp2_json[9]['close']
    print('Проверяем изменение цены за десять свечей')
    print(f'now: {resp_close_now} ten candels later:  {resp_close_ten}')
    if abs(resp_close_ten - resp_close_now) >= 300:  # 500 нужный параметр
        print('Переходим к проверке разворотной свечи')
        i = 1
        return reversal_candle(i)
    else:
        print('ждем минуту до формирования следующей свечи')
        time_mod()
        return print('переходим опять в чек вольюм'), check_trades()


def reversal_candle(i):
    # Проверка на нужный вектор свечи
    time_mod()
    url3 = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=2&reverse=true'
    resp = requests.get(url3).text
    data = json.loads(resp)
    print('После запроса и вычислений на разворотную свечу получаем: ')
    data_new_op = data[0]['open']
    data_new_cl = data[0]['close']
    data_new_high_bitcoin = data[0]['high']
    data_new_low_bitcoin = data[0]['low']
    data_old_op = data[1]['open']
    data_old_cl = data[1]['close']
    difference_old = data_old_cl - data_old_op  # Направление старой свечи
    difference_new = data_new_cl - data_new_op  # Направление новой разворотной свечи
    reversal_candle_value = difference_new
    print('difference_old', difference_old)
    print('difference_new', difference_new)

    if (difference_old > 0) and (difference_new < 0):  # разворотная свеча красная
        print('Разворотная свеча сформирована (красная)')
        print('Переходим к функции открывающей ордер1')
        data_new_bitcoin = data_new_low_bitcoin - 10
        orderQty = -1
        return fun_open_order(orderQty, data_new_bitcoin, reversal_candle_value)

    elif (data_old_cl - data_old_op < 0) and (data_new_cl - data_new_op > 0):  # разворотная свеча зелёная
        print('Разворотная свеча сформирована (зеленая)\nПереходим к функции открывающей ордер2')
        data_new_bitcoin = data_new_high_bitcoin + 10
        orderQty = 1  # Для биткоина 100 минимум и кратно 100
        return fun_open_order(orderQty, data_new_bitcoin, reversal_candle_value)

    elif i < 5:  # нужный параметр 5
        print(f'У Нас две одинаковые по цвету свечи, ждем следущую. Проход № {i}')
        i += 1
        print(f'заходим в reversal_candle({i})')
        reversal_candle(i)
    else:
        print('Из 5-ти свечей нет пеперодной\nПереходим к началу программы')
        check_trades()  # Переходим в начало программы


# -------------------------------------------------------------------------------------------------


def fun_open_order(orderQty, data_new_bitcoin, reversal_candle_value):  # Сформирована разворотная свеча
    print('Перешли в функцию - fun_open_stop_order')
    if reversal_candle_value<0:
        color = 'красная'
    else:
        color = 'зеленая'
    print(
        f'сторона: {orderQty},макс или мин биткоин: {data_new_bitcoin}\n'
        f',цвет разворотной свечи: {color}')

    print('Переходим к слежению за ценой - check_activ_ord ')
    check_activ_ord(orderQty, data_new_bitcoin, reversal_candle_value)
    print('Переходим к слежению за открытым ордером')

#-------------------------------------------------------------------------------------------------

def check_activ_ord(orderQty, data_new_bitcoin, reversal_candle_value):
    # Следим за ценой и открываем ордер
    k = 1
    while True:
        url = 'https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&count=1&reverse=true'

        resp = requests.get(url).text
        data = json.loads(resp)
        data1 = (data[0]['price'])
        print(k,data1)
        time.sleep(2)
        k+=1
        if orderQty < 0: # Если ордер на продажу
            if data1 <= data_new_bitcoin:
                print('Открываем маркет на продажу')
                return new_market_order(orderQty)
            elif k > 28:  # 28 проходов затем пойдет следующая минута
                print('Прошло 5 минут а ордер не открыт ждем\n'
                      ' формирования следующей разворотной свечи')
                print('Переходим в reversal_candle_comparison')
                return reversal_candle_comparison(reversal_candle_value, i=1)
        elif orderQty > 0: # Если ордер на покупку
            if data1 >= data_new_bitcoin:
                print('Открываем маркет на покупку')
                return new_market_order(orderQty)
            elif k > 28:  # 28 проходов затем пойдет следующая минута
                print('Прошло 5 минут а ордер не открыт ждем\n'
                      ' формирования следующей разворотной свечи')
                print('Переходим в def reversal_candle_comparison')
                return reversal_candle_comparison(reversal_candle_value, i=1)



def reversal_candle_comparison(reversal_candle_value,i):
    # Сверяем значение разворотной свечи со следующей

    print(f'Мы вошли в reversal_candle_comparison проход № {i}')
    url3 = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=2&reverse=true'# Поменять на XBT
    resp = requests.get(url3).text
    data = json.loads(resp)
    print('r_c_c После запроса и вычислений на разворотную свечу получаем: ')
    data_new_op_bit = data[0]['open']
    data_new_cl_bit = data[0]['close']
    data_new_high = round((data[0]['high']),4)
    data_new_low = round((data[0]['low']),4)
    difference_new = data_new_cl_bit - data_new_op_bit
    print('reversal_candle_value', reversal_candle_value)
    print('difference_new', difference_new)

    if ((reversal_candle_value > 0) and (difference_new < 0)) or ( # Если свеча противоположная разворотной, то ждем 5 мин
            (reversal_candle_value < 0) and (difference_new > 0)):
        time_mod()
        i += 1
        if i < 5:
            reversal_candle_comparison(reversal_candle_value, i) # Переходим в начало функции с i+1
        else:
            print('За пять свечей так и не сформировалась разворотная\nПереходим в начало программы')
            check_trades()# Поставить переход в начало программы check_order()

    else: # Если свеча совпадает с разворотной, то переходим в check_activ_ord(reversal_candle_value)
        # передать параметры новой свечи хай или лоу в зависимости от цвета.Зеленая - хай и по ней выставим стоп-ордер на покупку
        if data_new_cl_bit - data_new_op_bit < 0: # Красная свеча
            price = data_new_low - 10
            check_activ_ord(-1, price, reversal_candle_value)
        else:                                     # Зеленая свеча
            price = data_new_high + 10
            check_activ_ord(1, price, reversal_candle_value)

# --------------------------------------------------------------------------------------------------

def new_market_order(orderQty):
    print(f'Мы вошли в функцию new_market_order сторона: {orderQty}')
    resp = requests.get(
        'https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=5&reverse=true')
    resp_json = resp.json()
    df = pd.DataFrame(resp_json)
    df.to_excel(f'./open order {orderQty} .xlsx', index=False)

# --------------------------------------------------------------------------------------------------

def time_mod():
    print('Ждем минуту ')
    time.sleep(1)
    while True:
        local_time = time.localtime().tm_sec
        time.sleep(0.5)
        if local_time == 15:
            return


def time_now():
    time_h = time.localtime().tm_hour
    time_m = time.localtime().tm_min
    time_s = time.localtime().tm_sec
    return f'{time_h}:{time_m}:{time_s}'


if __name__ == '__main__':
    print('Запуск программы')
    check_trades()

print('the end')