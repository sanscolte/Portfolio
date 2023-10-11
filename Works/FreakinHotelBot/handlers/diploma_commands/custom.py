from bot import bot
from logging import basicConfig, DEBUG
from database.create_data_funcs import create_record
from database.models import User, History
from handlers.diploma_commands.request_funcs import api_request
from states.info_states import CustomCommand
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from requests.exceptions import ReadTimeout
from typing import Dict, List, Any

basicConfig(level=DEBUG,
            filename='logs.log',
            format='%(asctime)s %(levelname)s %(message)s')


@bot.message_handler(commands=['custom'])
def input_custom_city(message: Message) -> None:
    """ Запрос города """

    create_record(model=User,
                  ID=message.from_user.id,
                  name=message.from_user.full_name
                  )
    bot.set_state(user_id=message.from_user.id,
                  state=CustomCommand.input_custom_city,
                  chat_id=message.chat.id)

    bot.send_message(message.chat.id, '🏙 Пожалуйста, введи город (en_US)')


@bot.message_handler(state=CustomCommand.input_custom_city)
def get_price_range(message: Message) -> None:
    """ Получение диапазона цены """

    if not message.text.isalpha():
        bot.send_message(chat_id=message.chat.id, text='❕ Что-то не так с городом...')

    else:
        city = str(message.text)

        bot.set_state(user_id=message.from_user.id,
                      state=CustomCommand.price_range,
                      chat_id=message.chat.id)

        bot.send_message(chat_id=message.chat.id, text='Good job!\nТеперь введи диапазон'
                                                       ' стоимости отеля через пробел ($)')

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as hotels:
            hotels['city']: str = city


@bot.message_handler(state=CustomCommand.price_range)
def get_custom_hotels(message: Message) -> None:
    """ Получение города и выдача пользователю списка актуальных отелей от центра """

    if ' ' not in message.text:
        bot.send_message(chat_id=message.chat.id, text='❕ Что-то не так с диапазоном стоимости...')

    else:
        answer: List[str] = message.text.split()

        if not answer[0].isdigit() or not answer[1].isdigit():
            bot.send_message(chat_id=message.chat.id, text='❕ Что-то не так с диапазоном стоимости...')

        else:
            min_price: int = int(answer[0])
            max_price: int = int(answer[1])

            bot.set_state(user_id=message.from_user.id,
                          state=CustomCommand.get_custom_list,
                          chat_id=message.chat.id)
            bot.send_message(chat_id=message.chat.id, text='⏳ Загружаю данные...')

            with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as hotels:
                city: str = hotels['city']

            params: Dict[str] = {"q": city}

            try:
                response = api_request(method_endswith='locations/v3/search',
                                       params=params,
                                       method_type='GET').json()

                create_record(model=History,
                              name=message.from_user.full_name,
                              ID=message.from_user.id,
                              message=city,
                              response=response
                              )

                gaia_id: str = response['sr'][0]['gaiaId']

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
                                           'sort': 'DISTANCE',
                                           'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
                                           }

                response = api_request(method_endswith='properties/v2/list',
                                       method_type='POST',
                                       payload=payload).json()

                hotels_from_api: Dict[Any] = response['data']['propertySearch']['properties']

                hotels_markup = InlineKeyboardMarkup()

                qty_of_list: int = 0
                for i_hotel in hotels_from_api:
                    hotel_name: str = i_hotel['name']
                    cur_price: str = i_hotel['price']['options'][0]['formattedDisplayPrice']
                    id_hotel: str = i_hotel['id']

                    if min_price <= int(cur_price[1:]) <= max_price:
                        qty_of_list += 1
                        hotels_markup.add(InlineKeyboardButton(text=f'{hotel_name} 🏷 {cur_price}',
                                                               callback_data=f'{hotel_name} --- {id_hotel}'))

                if qty_of_list:
                    bot.send_message(chat_id=message.chat.id,
                                     text='🏨 Список актуальных отелей по удаленности '
                                          'от центра в {city}\n'
                                          '🔎 Выбери нужный отель для получения подробностей'.format(
                                         city=city),
                                     reply_markup=hotels_markup
                                     )
                    hotels.clear()

                    bot.set_state(user_id=message.from_user.id,
                                  state=CustomCommand.get_custom_detail,
                                  chat_id=message.chat.id)

                else:
                    bot.send_message(chat_id=message.chat.id, text='❔ Отелей не найдено :(')

            except (ReadTimeout, AttributeError):
                bot.send_message(chat_id=message.chat.id,
                                 text='📉 Время ожидания от сервера превышено, попробуй еще раз')


@bot.callback_query_handler(func=lambda call: True)
@bot.message_handler(state=0)
def get_custom_detail(call) -> None:
    """ Выдача пользователю подробностей о выбранном отеле """

    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as hotels:
        hotels['ID']: str = call.data.split(' --- ')[1]
        hotels['name']: str = call.data.split(' --- ')[0]
        ID: str = hotels['ID']
        hotel_name: str = hotels['name']

    bot.send_message(chat_id=call.message.chat.id, text='⏳ Загружаю детальные данные...')

    payload: Dict[str, int] = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": ID
    }

    try:
        response = api_request(method_endswith='properties/v2/detail',
                               method_type='POST',
                               payload=payload).json()

        create_record(model=History,
                      name=call.message.from_user.full_name,
                      ID=call.message.from_user.id,
                      message=hotel_name,
                      response=response
                      )

        try:

            with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as hotels:
                hotels['details']: List[str] = [
                    response['data']['propertyInfo']['summary']['name'],
                    response['data']['propertyInfo']['summary']['tagline'],
                    f"Address: {response['data']['propertyInfo']['summary']['location']['address']['addressLine']}",
                ]

            hotel_photo: str = response['data']['propertyInfo']['propertyGallery']['images'][0]['image']['url']

            if hotels['details']:
                bot.send_message(chat_id=call.message.chat.id, text='\n'.join(hotels['details']))
                bot.send_photo(chat_id=call.message.chat.id, photo=hotel_photo)
                bot.send_message(chat_id=call.message.chat.id, text='Приятного отдыха!')
                bot.delete_state(user_id=call.message.from_user.id, chat_id=call.message.chat.id)

            else:
                bot.send_message(call.message.chat.id, '❔ Такого ID не найдено :(')

        except TypeError:
            bot.send_message(chat_id=call.message.chat.id, text='❕Что-то не так с ID...')

    except ReadTimeout:
        bot.send_message(chat_id=call.message.chat.id, text='📉 Время ожидания от сервера превышено, попробуй еще раз')
