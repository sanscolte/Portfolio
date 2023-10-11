from bot import bot
from logging import basicConfig, DEBUG
from keyboards.reply.contact import request_phone_number
from states.info_states import UserInfoState
from telebot.types import Message

basicConfig(level=DEBUG,
            filename='logs.log',
            format='%(asctime)s %(levelname)s %(message)s')


@bot.message_handler(commands=['survey'])
def survey_command(message: Message) -> None:
    """ Запрос имени пользователя """
    bot.set_state(user_id=message.from_user.id,
                  state=UserInfoState.name,
                  chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id,
                     text=f'👋🏻 Привет, {message.from_user.username}! Скажи мне свое имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    """ Получение имени пользователя и запрос возраста """
    if not message.text.isalpha():
        bot.send_message(chat_id=message.from_user.id,
                         text='❕ Имя может содержать только буквы!')

    else:
        bot.reply_to(message=message, text='Nice!\nТеперь введи свой возраст')
        bot.set_state(user_id=message.from_user.id,
                      state=UserInfoState.age,
                      chat_id=message.chat.id)

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as user_data:
            user_data['name']: str = message.text


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    """ Получение возраста пользователя и запрос номера телефона """
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, '❕ Возраст может быть только числом!')

    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Good job!\n📲 Теперь отправь свой номер телефона, нажав на кнопку',
                         reply_markup=request_phone_number())
        bot.set_state(user_id=message.from_user.id,
                      state=UserInfoState.phone_number,
                      chat_id=message.chat.id)

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as user_data:
            user_data['age']: str = message.text


@bot.message_handler(content_types=['text', 'contact'], state=UserInfoState.phone_number)
def get_phone_number(message: Message) -> None:
    """ Получение номера телефона пользователя """
    if not message.content_type == 'contact':
        bot.send_message(chat_id=message.chat.id,
                         text='🤷🏼‍♂️ Как хочешь, но если что кнопка внизу')

    else:

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as user_data:
            user_data['phone_number']: str = message.contact.phone_number

            thanks_data: str = f'🎉 Спасибо! \n' \
                               f'Вот твои данные:\n\n' \
                               f'Имя {"-" * 5} {user_data["name"]}\n' \
                               f'Возраст {"-" * 5} {user_data["age"]}\n' \
                               f'Номер телефона {"-" * 5} {user_data["phone_number"]}'

            bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
            bot.send_message(chat_id=message.chat.id, text=thanks_data)
