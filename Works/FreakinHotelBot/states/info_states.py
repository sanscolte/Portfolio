from telebot.handler_backends import StatesGroup, State


class UserInfoState(StatesGroup):
    """
    Дочерний класс пользователя UserInfoState. Родитель: StatesGroup

    Attributes:
        name (State): Имя пользователя
        age (State): Возраст пользователя
        phone_number (State): Номер телефона пользователя
    """

    name = State()
    age = State()
    phone_number = State()


class LowCommand(StatesGroup):
    """
    Дочерний класс пользователя LowCommand. Родитель: StatesGroup

    Attributes:
        input_low_city (State): Город для запроса
        max_price (State): Максимальная стоимость отеля
        get_low_list (State): Получение списка отелей
        get_low_detail (State): Получение подробностей об отеле
    """

    input_low_city = State()
    max_price = State()
    get_low_list = State()
    get_low_detail = State()


class HighCommand(StatesGroup):
    """
    Дочерний класс пользователя LowCommand. Родитель: StatesGroup

    Attributes:
        input_high_city (State): Город для запроса
        min_price (State): Минимальная стоимость отеля
        get_high_list (State): Получение списка отелей
        get_high_detail (State): Получение подробностей об отеле
    """

    input_high_city = State()
    min_price = State()
    get_high_list = State()
    get_high_detail = State()


class CustomCommand(StatesGroup):
    """
    Дочерний класс пользователя LowCommand. Родитель: StatesGroup

    Attributes:
        input_custom_city (State): Город для запроса
        price_range (State): Ценовой диапазон стоимости отеля
        get_custom_list (State): Получение списка отелей
        get_custom_detail (State): Получение подробностей об отеле
    """

    input_custom_city = State()
    price_range = State()
    get_custom_list = State()
    get_custom_detail = State()
