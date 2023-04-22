import requests
import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN='5896626762:AAHGpDL53QbVY9uwareE3rpiYUKy4ouhAQY'

async def level(ticker):  # https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data
    url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval=1m&limit=140' # &startTime={unix_time()}
    resp = requests.get(url)
    resp_j = resp.json()
    high_list = []
    low_list = []
    count = 0
    high_last = float(resp_j[-1][2])
    print('high_last',high_last)
    pers = high_last * 0.00035
    for el in resp_j:
        high = el[2]
        low = el[3]
        high_list.append({count: high})
        low_list.append({count: low})
        count+=1
    # Сортировка списка лоу по второму значению
    low_tuple_list = [(k, float(v)) for d in low_list for k, v in d.items()]
    low_sorted_tuple_list = sorted(low_tuple_list, key=lambda x: x[1])
    low_sorted_dict = {t[0]: t[1] for t in low_sorted_tuple_list}
    # Сортировка списка хай по второму значению
    high_tuple_list = [(k, float(v)) for d in high_list for k, v in d.items()]
    high_sorted_tuple_list = sorted(high_tuple_list, key=lambda x: x[1], reverse=True)
    high_sorted_dict = {t[0]: t[1] for t in high_sorted_tuple_list}

    # Сортировка максимумов
    for i in range(0,3):
        llist_del = []
        counter = 0
        big_one = 500
        for el in high_sorted_dict:
            if counter == i:
                big_one = el
                counter += 1
            if abs(big_one - el) < 21 and big_one != el:
                llist_del.append(el)
            counter +=1
        for el in llist_del:
            del high_sorted_dict[el]

    counter = 0 # Оприделение уровней.Если разница уровней близка к нулю то это level
    higher_list = []
    for el in high_sorted_dict:
        if counter < 3:
            higher_list.append(high_sorted_dict[el])
            counter +=1
    print('higher_list', higher_list)
    h1 = higher_list[0]
    h2 = higher_list[1]
    h3 = higher_list[2]
    if abs(h1-h2)<=pers and abs(h1-h3)<=pers or abs(h1-h2)<=pers and abs(h2-h3)<=pers: #Если растояние между 3 мя хаями не больше 15ти, то это хороший уровень
        return (f'{ticker} Level up with 3 point {h1}')
    if abs(h1-h2)<=pers or abs(h1-h3)<=pers:
        return (f'{ticker} Level up with 2 point {h1}')
    if abs(h2-h3)<=pers:
        return (f'{ticker} Level up with 2 point.2 and 3-level  {h2}')

    # Сортировка минимумов
    for i in range(0,3):
        llist_del = []
        counter = 0
        small_one = 500
        for el in low_sorted_dict:
            if counter == i:
                small_one = el
                counter += 1
            if abs(small_one - el) < 21 and small_one != el:
                llist_del.append(el)
            counter +=1
        for el in llist_del:
            del low_sorted_dict[el]

    counter = 0
    lower_list = []
    for el in low_sorted_dict:
        if counter < 3:
            lower_list.append(low_sorted_dict[el])
            counter += 1
    print('lower_list', lower_list)
    l1 = lower_list[0]
    l2 = lower_list[1]
    l3 = lower_list[2]
    if abs(l1 - l2) <= pers and abs(l1 - l3) <= pers or abs(l1 - l2) <= pers and abs(
            l2 - l3) <= pers:  # Если растояние между 3 мя хаями не больше 15ти, то это хороший уровень
        return(f'{ticker} Level low with 3 point {l1}')
    if abs(l1 - l2) <= pers or abs(l1 - l3) <= pers or abs(l2 - l3) <= pers:
        print('Level low with 2 point')
        return(f'{ticker} Level low with 2 point {l1}') #сделать return
    if abs(l2 - l3) <= pers:
        print('Level low with 2 point 2 and 3')
        return (f'{ticker} Level low with 2 point.2 and 3-level {l2}')  # сделать return
    else:
        return 0



async def time_mod():
    print('waiting for a new minute')
    # waiting for a new minute
    await asyncio.sleep(60)



async def send_message_on_success(bot: Bot, chat_id: int):
    print('send_message_on_success')
    ticker_list = ['BTCUSDT', 'ETHUSDT', 'LINKUSDT','LTCUSDT','ETCUSDT']
    message_list = []
    while True:
        counter = 0
        await time_mod()
        while True:
            if counter == len(ticker_list):
                break
            ticker = ticker_list[counter]
            counter+=1
            mes = await level(ticker)
            if mes != 0:
                await bot.send_message(chat_id=chat_id, text=mes)




async def main():
    # Создаем объект бота
    bot = Bot(token=TOKEN)
    chat_id = 739957796
    # Создаем объект Dispatcher
    dp = Dispatcher(bot)

    # Запускаем функцию, которая будет отправлять сообщения при удачном запросе
    await send_message_on_success(bot, chat_id)



if __name__ == '__main__':
    asyncio.run(main())
