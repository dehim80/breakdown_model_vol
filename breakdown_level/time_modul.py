import time


def time_mod():
    # Функция ждет, пока минуты будут кратные пяти. Затем выходит из функции.
    loc_hour = time.localtime().tm_hour
    loc_min = time.localtime().tm_min

    print(f'Мы зашли в фунцию time_mod {loc_hour}:{loc_min}')
    time.sleep(100)
    while True:
        local_time = time.localtime().tm_min
        loc2 = local_time % 5
        if (loc2 == 0) or local_time == 0:
            time.sleep(5)
            return
        else:
            time.sleep(10)


def time_mod_midnight():
    # Следит за временем в 04-30 делает return
    loc_hour = time.localtime().tm_hour
    if loc_hour >= 4 and loc_hour <= 23:
        return
    while True:
        loc_hour = time.localtime().tm_hour
        loc_min = time.localtime().tm_min
        print(f'Мы зашли в функцию time_mod_midnight {loc_hour}:{loc_min}')
        if loc_hour == 4 and loc_min == 30:  # Должно быть loc_hour == 4 loc_min == 0
            return
        else:
            time_mod()
        print(f'Мы вернулись в функцию time_mod_midnight {loc_hour}:{loc_min}')


def time_now():
    print('Зашли в функцию time_nowW')
    loc_hour = time.gmtime().tm_hour
    loc_min = time.gmtime().tm_min
    loc_date = time.gmtime().tm_mday
    loc_month = time.gmtime().tm_mon
    loc_year = time.gmtime().tm_year
    return (f'{loc_year}-{loc_month}-{loc_date}%20{loc_hour}%3A{loc_min}')


def date_now():
    loc_year = time.gmtime().tm_year
    loc_month = time.gmtime().tm_mon
    loc_date = time.gmtime().tm_mday
    return (f'{loc_year}-{loc_month}-{loc_date}')


# if __name__ == '__main__':
#     print(time_four_hours_ago())
#     print(time_now())
