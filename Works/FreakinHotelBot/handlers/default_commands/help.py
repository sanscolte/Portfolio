from bot import bot
from logging import basicConfig, DEBUG
from database.create_data_funcs import create_record
from database.models import User
from telebot.types import Message
from typing import List

commands: List[str] = ['❕ Список команд:',
                       '⬇️ /low — Минимальные стоимость',
                       '⬆️ /high — Максимальная стоимость',
                       '↕️ /custom — Сортировка от центра)',
                       '📊 /history — История запросов',
                       '❔ /help — Команды бота',
                       '📝 /survey - Опрос']

basicConfig(level=DEBUG,
            filename='logs.log',
            format='%(asctime)s %(levelname)s %(message)s')


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    """ Функция, выводящая команды бота """
    create_record(model=User,
                  name=message.from_user.full_name,
                  ID=message.from_user.id,
                  )
    bot.send_message(message.chat.id, '\n'.join(commands))
