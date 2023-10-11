"""
from logging import basicConfig, DEBUG
from bot import bot
from telebot.types import Message

basicConfig(level=DEBUG,
            filename='logs.log',
            format='%(asctime)s %(levelname)s %(message)s')


@bot.message_handler(state=None)
def echo_command(message: Message) -> None:
    ''' Функция, возвращающая ответ пользователя '''
    bot.send_message(message.chat.id, message.text)
"""
