from dotenv import load_dotenv, find_dotenv
from typing import Tuple
from os import getenv

if not find_dotenv():
    exit('Отсутствует файл .env :/')
else:
    load_dotenv()

TOKEN: str = getenv('TOKEN')
API_KEY: str = getenv('KEY')

COMMANDS: Tuple = (
    ('start', 'Запустить бота!'),
    ('help', 'Вывести справку'),
    ('low', 'Низкая стоимость'),
    ('high', 'Высокая стоимость'),
    ('custom', 'От центра'),
    ('history', 'История запросов'),
    ('survey', 'Опрос'),
)
