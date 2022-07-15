import pandas as pd
import requests


def sample_size():  # Чекает цену за последние ??? свечей и выбирает нужную модель
    print('Мы в функции model_classifications')
    for i1 in range(00,59):
        i2=i1+1

    resp = requests.get('https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&columns=side%2C%20size%2C%20price&'
                        'count=1000&reverse=false&startTime=2022-07-15%2001%3A53&endTime=2022-07-15%2001%3A54')
    print(type(resp))
    resp_json = resp.json()
    print(resp_json) # type list
    print('lenght= ',len(resp_json))
    print(type(resp_json[0]))

    sample_size = []


    for i in range(len(resp_json)):
        if resp_json[i]['size']>9000:
            sample_size.append(resp_json[i])
    print(sample_size)

    df = pd.DataFrame(sample_size)
    df.to_excel('./hist2022-07-15 01-53.xlsx', index=False)


if __name__ == '__main__':
    sample_size()

    # делаем лист куда будут складыватся трейды выше 150К в конце прогона лист пишем в файл
    # автоматически подставляем время- минута+1 прогоняем записываем в файл
    # Прогнать как можно больше истории и посмотреть сколько больших трейдов вообще проходит в тихой обстановке
    # Стоит ли прикручивать пробой уровня или можно просто чекнуть мега уровень и войти в сделку