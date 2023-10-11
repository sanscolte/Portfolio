from telebot.types import BotCommand
from config.config import COMMANDS


def set_commands(bot) -> None:
    """
    Функция, устанавливающая команды бота в меню

    :param bot: Бот
    """
    bot.set_my_commands([BotCommand(*command) for command in COMMANDS])
