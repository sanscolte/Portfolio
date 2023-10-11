from logging import basicConfig, DEBUG
from bot import bot
from database.create_data_funcs import create_record
from database.models import User
from telebot.types import Message

basicConfig(level=DEBUG,
            filename='logs.log',
            format='%(asctime)s %(levelname)s %(message)s')


@bot.message_handler(commands=['start'])
def start_command(message: Message) -> None:
    """ Функция приветствия """
    create_record(model=User,
                  name=message.from_user.full_name,
                  ID=message.from_user.id,
                  )
    bot.send_message(message.chat.id, f'👋🏻 Привет, {message.from_user.full_name}!')
