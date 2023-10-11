from bot import bot
from logging import basicConfig, DEBUG
from telebot.types import Message
from typing import List
from database.models import History

basicConfig(level=DEBUG,
            filename='logs.log',
            format='%(asctime)s %(levelname)s %(message)s')


@bot.message_handler(commands=['history'])
def history_command(message: Message) -> None:
    """ Функция, возвращающая последние 10 запросов пользователя """
    last_ten_elem: List[str] = []

    for i_data in History.select().where(History.tg_id == message.from_user.id):
        last_ten_elem.append(i_data.message)

    if last_ten_elem:
        bot.send_message(chat_id=message.chat.id,
                         text='📊 Ваши последние 10 запросов:\n\n{requests}'.format(
                             requests='\n'.join(reversed(last_ten_elem[-10:]))))
    else:
        bot.send_message(chat_id=message.chat.id, text='📃 Ваша история пуста')
