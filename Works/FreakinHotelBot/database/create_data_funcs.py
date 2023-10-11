from database.models import db, User, History
from requests.models import Response
from typing import TypeVar


def create_tables() -> None:
    """ Функция создания таблицы User """
    User.create_table()
    History.create_table()


def create_record(model: TypeVar,
                  ID: int,
                  name: str,
                  response: Response = None,
                  message: str = None,
                  db=db) -> None:
    """
    Функция записи данных в таблицу

    :param model: Таблица записи
    :param ID: Telegram ID пользователя
    :param name: Имя пользователя
    :param response: Ответ от сервера
    :param message: Ответ пользователя
    :param db: База хранения данных
    :type model: TypeVar
    :type ID: int
    :type name: str
    :type response: Response
    :type message: str
    """

    if model == User:
        if not User.select().where(User.tg_id == ID):
            with db:
                User.create(name=name, tg_id=ID)
    else:
        with db:
            History.create(name=name, tg_id=ID, message=message, response=response)
