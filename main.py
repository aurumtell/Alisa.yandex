from flask import Flask, request
import logging
import json

from api import get_avia,get_avia_cheap,get_iata


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.decidedToBuy = False
        self.fromCity = None
        self.toCity = None
        self.directionSelected = False
        self.fromDate = None
        self.toDate = None
        self.dateSelected = False

    def isDecidedToBuy(self):
        return self.decidedToBuy

    def get_name(self):
        return self.name

    def setFromTo(self, fromCity, toCity):
        self.fromCity = fromCity
        self.toCity = toCity
        self.directionSelected = True


user = None

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


sessionStorage = {}


def log():
    logging.debug('Debug')
    logging.info('Info')
    logging.warning('Warning')
    logging.error('Error')
    logging.critical('Critical or Fatal')


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    global user
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # созда\м словарь в который в будущем положим имя пользователя
        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь ещё не представился.
    if user is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            user = User(user_id, first_name)
            res['response'][
                'text'] = 'Приятно познакомиться, ' + first_name.title() \
                          + '. Я - Алиса. Вы хотите куда-нибудь полететь?Пишите "Хочу билет"'
            # res['response']['buttons'] = ['yes','sd']
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] = [{
                'title': 'да',
                'hide': True
                },
                {
                'title': 'хочу',
                'hide': True
                }]

            log()

    # если мы знакомы с пользователем и он нам что-то написал,
    # то это говорит о том, что он уже говорит о городе, что хочет увидеть.
    else:
        if req['request']['original_utterance'].lower() in [
            'да',
            'хочу',
            'хочу билет'
        ]:
            user.decidedToBuy = True
            res['response']['text'] = 'Назовите город вылета и город назначения'

        elif user.decidedToBuy:
            if req['request']['original_utterance'].lower() in [
                'нет',
                'не хочу',
            ]:
                res['response']['text'] = 'Хорошо, обращайтесь, если запланируете поездку!'
            elif not user.directionSelected:
                cities = get_city(req)

                print(cities)

                if len(cities) == 1:
                    res['response']['text'] = 'Ты написал только город назначения'
                if len(cities) == 2:
                    user.setFromTo(cities[0], cities[1])
                    res['response']['text'] = 'Назовите дату вылета'
                elif len(cities) > 2:
                    res['response']['text'] = 'Слишком много городов!'
            elif user.directionSelected:
                if get_date(req) is not None:
                    res['response']['text'] = 'Вам нужны дешевые авивабилеты?Если да, то напишите "дешевые", ' \
                                              'если нет, то "не дешевые" '
                    res['response']['buttons'] = [{
                        'title': 'дешевые',
                        'hide': True
                        },
                        {
                        'title': 'не дешевые',
                        'hide': True
                        }]
                    date = get_date(req)
                    user.fromDate = date
                elif req['request']['original_utterance'].lower() == 'не дешевые':
                    city_origin_code, city_destination_code = get_iata(user.fromCity, user.toCity)
                    avia = get_avia(city_origin_code, city_destination_code, user.fromDate)
                    res['response']['text'] = 'дата вылета:'+avia[0][4]+' '+'количество пересадок:' + avia[0][6]+' '+'цена:' + avia[0][7]
                    res['response']['buttons'] = [{
                        'title': 'покупай!',
                        'hide': True,
                        'url': 'http://www.aviasales.ru/?search=multi&marker=УкажитеЗдесьВашМаркер'
                        }]
                elif req['request']['original_utterance'].lower() == 'дешевые':
                    print('cheap')
                    city_origin_code, city_destination_code = get_iata(user.fromCity, user.toCity)
                    avia = get_avia_cheap(city_origin_code, city_destination_code, user.fromDate)
                    res['response']['text'] = 'цена:'+avia[0]+' '+'номер рейса:' + avia[2]+' '+'дата вылета:' + avia[3]
                    res['response']['buttons'] = [{
                        'title': 'покупай!',
                        'hide': True,
                        'url': 'http://www.aviasales.ru/?search=multi&marker=УкажитеЗдесьВашМаркер'
                        }]
        else:
            res['response']['text'] = 'Хорошо, обращайтесь, если запланируете поездку!'


def get_city(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


def get_date(req):
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.DATETIME
        if entity['type'] == 'YANDEX.DATETIME':
            return entity['value'].get('month', None), entity['value'].get('day', None)


if __name__ == '__main__':
    app.run()
