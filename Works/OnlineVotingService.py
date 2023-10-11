from typing import Dict

models: Dict = {}


def voting() -> None:
    """ Функция запуска проведения голосования """
    while True:
        vote: str = input('\nВаш выбор?: ')
        if vote != '0':
            if vote not in models.keys():
                print('Такой модели нет в вариантах голосования!')
            else:
                models[vote] += 1
                print('Ваш голос принят!')
        else:
            break
    print('\nГолосование завершено!')
    print(f'Лучший автомобиль года: {result()[0]}')
    print(f'Количество голосов: {result()[1]}')


def result() -> (str, int):
    """ Функция получения результата голосования. Возвращает модель и кол-во голосов """
    res: int = max(models, key=models.get)
    return res, models[res]


def start() -> None:
    """ Функция запуска голосования """
    print('Голосование за автомобиль года\n')

    while True:
        try:
            qty_of_models: int = int(
                input('Сколько моделей авто участвуют в голосовании?: '))
            break
        except ValueError:
            pass
    for i_model in range(qty_of_models):
        model: str = input(f'Введите модель {i_model + 1}-го автомобиля: ')
        models[model] = 0
    print('\nГолосование создано!')
    print(f'Выберите модель из списка: {"; ".join(models.keys())}')
    print('Для подсчета голосов введите 0')
    voting()


start()
