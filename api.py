import requests


def get_avia_cheap(city_origin_code, city_destination_code, date):
    try:
        if date[0] >= 10:
            date = '2019'+'-'+str(date[0])
        else:
            date = '2019'+'-'+ '0'+str(date[0])
        # url, по которому доступно API Яндекс.Карт
        url = "http://api.travelpayouts.com/v1/prices/direct"
        params = {
            # город, координаты которого мы ищем
            'origin': city_origin_code,
            # формат ответа от сервера, в данном случае JSON
            'destination': city_destination_code,
            'depart_date': date[0],
            'token': '3adecc4f29fece71a7d27292750887d2'
        }

        # отправляем запрос
        response = requests.get(url, params)
        print(requests.get(url, params).text)
        # получаем JSON ответа
        json = response.json()
        print(json)
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
        if date[0] < 10:
            date[0] = '0' + date[0]
        if date[1] < 10:
            date[1] = '0' + date[1]
        date = '2019'+'-'+ str(date[0])+'-'+str(date[1])
        # url, по которому доступно API Яндекс.Карт
        url = "http://api.travelpayouts.com/v2/prices/week-matrix"
        # параметры запроса
        params = {
            # город, координаты которого мы ищем
            'origin': city_origin_code,
            # формат ответа от сервера, в данном случае JSON
            'destination': city_destination_code,
            'depart_date': date,
            'return date': date,
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


        return avia
    except Exception as e:
        return e


def get_iata(city1, city2):
    try:
        # url, по которому доступно API Яндекс.Карт
        url = "https://www.travelpayouts.com/widgets_suggest_params"
        # параметры запроса
        search = 'из' + city1+ 'в' + city2
        params = {
            # город, координаты которого мы ищем
            'q': search,
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
        iata1 = json['origin'][0]['name']
        iata2 = json['origin'][1]['name']
        # Превращаем string в список, так как точка -
        # это пара двух чисел - координат
        return iata1, iata2
    except Exception as e:
        return e
