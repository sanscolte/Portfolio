from bot import bot
from database.create_data_funcs import create_tables
from utils.set_commands import set_commands
from telebot.custom_filters import StateFilter
import handlers  # noqa

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    create_tables()
    set_commands(bot)
    bot.infinity_polling()
