import requests
def test():
    print('sdfghjk')

def get_avia_cheap(city_origin_code, city_destination_code, date):
    try:
        date = '2019'+'-'+ str(date)
        print('get avia')
        # url, по которому доступно API Яндекс.Карт
        url = "http://api.travelpayouts.com/v1/prices/direct"
        # параметры запроса
        params = {
            # город, координаты которого мы ищем
            'origin': city_origin_code,
            # формат ответа от сервера, в данном случае JSON
            'destination': city_destination_code,
            'depart_date': date,
            'token': '3adecc4f29fece71a7d27292750887d2',
            'format': 'json'
        }
        # отправляем запрос
        response = requests.get(url, params)
        # получаем JSON ответа
        json = response.json()
        # получаем координаты города (там написаны долгота(longitude),
        # широта(latitude) через пробел).
        # Посмотреть подробное описание JSON-ответа можно
        # в документации по адресу
        # https://tech.yandex.ru/maps/geocoder/
        avia = json['success'][1]['data']['HKT'][0]
        # Превращаем string в список, так как точка -
        # это пара двух чисел - координат

        return avia
    except Exception as e:
        return e

def get_avia(city_origin_code, city_destination_code, date):
    try:
        date = '2019'+'-'+ date
        # url, по которому доступно API Яндекс.Карт
        url = "http://api.travelpayouts.com/v2/prices/week-matrix"
        # параметры запроса
        params = {
            # город, координаты которого мы ищем
            'origin': city_origin_code,
            # формат ответа от сервера, в данном случае JSON
            'destination': city_destination_code,
            'depart_date': date,
            'token': '3adecc4f29fece71a7d27292750887d2'
        }
        # отправляем запрос
        response = requests.get(url, params)
        # получаем JSON ответа
        json = response.json()
        # получаем координаты города (там написаны долгота(longitude),
        # широта(latitude) через пробел).
        # Посмотреть подробное описание JSON-ответа можно
        # в документации по адресу
        # https://tech.yandex.ru/maps/geocoder/
        avia = json['success']['data']
        # Превращаем string в список, так как точка -
        # это пара двух чисел - координат

        return avia
    except Exception as e:
        return e


def get_iata(city):
    try:
        # url, по которому доступно API Яндекс.Карт
        url = "https://www.travelpayouts.com/widgets_suggest_params"
        # параметры запроса
        params = {
            # город, координаты которого мы ищем
            'q': city,
            'token': '3adecc4f29fece71a7d27292750887d2'
        }
        # отправляем запрос
        response = requests.get(url, params)
        # получаем JSON ответа
        json = response.json()
        # получаем координаты города (там написаны долгота(longitude),
        # широта(latitude) через пробел).
        # Посмотреть подробное описание JSON-ответа можно
        # в документации по адресу
        # https://tech.yandex.ru/maps/geocoder/
        iata = json['origin']['name']
        # Превращаем string в список, так как точка -
        # это пара двух чисел - координат
        print('iata')
        return iata
    except Exception as e:
        return e
