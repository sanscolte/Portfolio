from peewee import SqliteDatabase, Model, CharField, TextField, IntegerField

db = SqliteDatabase('database.db')


class BaseModel(Model):
    """ Дочерний класс BaseModel. Родитель: peewee.Model"""

    class Meta:
        """ Базовый класс Meta, хранящий базу хранения данных """
        database = db


class User(BaseModel):
    """
    Дочерний класс BaseModel. Родитель: BaseModel

    Args:
        :param name: Имя пользователя
        :param tg_id: Telegram ID пользователя
        :type name: str
        :type tg_id: int
    """

    class Meta:
        """ Базовый класс Meta, хранящий таблицу базы хранения данных """
        db_table: str = 'USERS'

    name: str = CharField()
    tg_id: int = IntegerField()


class History(User):
    """
    Дочерний класс History. Родитель: User

    Args:
        :param message: Ответ пользователя
        :param response: Ответ от сервера
        :type message: str
        :type response: str
    """

    class Meta:
        """ Базовый класс Meta, хранящий таблицу базы хранения данных """
        db_table: str = 'HISTORY'

    message: str = TextField()
    response: str = TextField()
