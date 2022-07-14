import pandas as pd
import requests


def write_in_exel(): # Чекает цену за последние ??? свечей и выбирает нужную модель
    print('Мы в функции model_classifications')
    resp = requests.get('https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&columns=open%2C%20close%2C%20high%2C%20low%2C%20trades%2C%20volume&count=500&reverse=false&'
                        'startTime=2022-07-13%202%3A00&endTime=2022-07-13%206%3A00')

    resp_json = resp.json()
    print(resp_json)
    df = pd.DataFrame(resp_json)
    df.to_excel('./hist130709-00.xlsx', index=False)


if __name__ == '__main__':
    write_in_exel()