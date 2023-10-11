from bot import bot
from handlers.diploma_commands.func import api_request
from requests import ReadTimeout
from telebot.types import Message
from typing import List, Dict, Any


@bot.message_handler(content_types=['text'])
def get_hotels(message: Message) -> None:
    """
    Запрос и выдача пользователю списка актуальных отелей

    :param message: город и стоимость
    :type message: str
    """

    try:
        answer: List[str] = message.split()
        city: str = answer[0]
        price: int = int(answer[1])
        if not price > 0:
            print('Стоимость отеля должна быть больше 0')
            return
        else:
            params: Dict[str] = {"q": city}
            print('Загружаю данные, пожалуйста, подожди...')

    except (IndexError, ValueError):
        bot.reply_to(message, 'Неправильный формат. Введи город (en_US)'
                              ' и мин. допустимую стоимость отеля через пробел')
        return

    try:
        response = api_request(method_endswith='locations/v3/search',
                               params=params,
                               method_type='GET')

        response = response.json()

    except ReadTimeout:
        print('Время ожидания превышено, попробуй еще раз')
        return

    try:
        gaia_id: str = response['sr'][0]['gaiaId']

    except (IndexError, KeyError, TypeError):
        print('Запрос не удался :(')
        return

    payload: Dict[str, int] = {'currency': 'USD',
                               'eapid': 1,
                               'locale': 'ru_RU',
                               'siteId': 300000001,
                               'destination': {
                                   'regionId': gaia_id
                               },
                               'checkInDate': {'day': 7, 'month': 12, 'year': 2022},
                               'checkOutDate': {'day': 9, 'month': 12, 'year': 2022},
                               'rooms': [{'adults': 1}],
                               'resultsStartingIndex': 0,
                               'resultsSize': 10,
                               'sort': 'RECOMMENDED',
                               'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
                               }

    try:
        response = api_request(method_endswith='properties/v2/list',
                               method_type='POST',
                               payload=payload)

        response = response.json()

        hotels_list: List[str] = []
        hotels_dict: Dict[Any] = response['data']['propertySearch']['properties']

    except ReadTimeout:
        print('Время ожидания превышено, попробуй еще раз')
        return

    for i_hotel in hotels_dict:
        name: str = i_hotel['name']
        cur_price: str = i_hotel['price']['options'][0]['formattedDisplayPrice']
        id_hotel: str = i_hotel['id']
        if int(cur_price[1:]) >= price:
            hotels_list.append(f'{name} {"-" * 5} {cur_price} {"-" * 5} {id_hotel}')

    if hotels_list:
        print('Список актуальных и рекомендуемых отелей '
              'от ${0} в {1}:\n\n{2}'.format(
            price, city, '\n'.join(hotels_list)
        ))
        hotels_list.clear()

    else:
        print('Отелей не найдено :(')
        return
