from typing import List, Dict, Callable

flights: Dict = {}
flight: List[str] = []


def validator(func: Callable, input_message: str, error_message: str) -> bool:
    while True:
        user_input: str = input(input_message)
        if func(user_input):
            flight.append(user_input.upper())
            return True
        print(error_message)


def print_cur_flight(flight_data: List[str], number: str) -> str:
    info: str = 'Информация о рейсе: '
    info += ' '.join(flight_data).strip()
    flights[number] = info
    return flights[number]


def print_flights() -> str:
    if flights:
        return '\n'.join(flights.values())
    return 'Информация о рейсах отсутствует'


def print_custom_flight(number: str) -> str:
    try:
        return flights[number]
    except KeyError:
        return f'Рейс {number} не найден'


def start():
    print('Сервис поиска авиабилетов\n')
    while True:
        print('\nГлавное меню:\n')
        print(
            '1 - ввод рейса\n2 - вывод всех рейсов\n3 - поиск рейса по номеру\n0 - завершение работы'
        )

        user_input: int = int(input('\nВведите номер пункта меню: '))

        if not user_input == 0:
            if user_input == 1:

                flight.clear()
                print('\nВведите данные рейса:')

                while True:
                    if len(flight_number := input(
                            'XXXX - номер рейса: ')) == 4 and flight_number.isalpha():
                        flight.append(flight_number.upper())
                        break
                    print('Номер рейса должен быть в формате XXXX!')

                validator(
                    func=lambda x: len(x) == 10 and (x[2:3] == '/', x[5:6] == '/') and
                                   (x.replace('/', '').isdigit()),
                    input_message='ДД/ММ/ГГГГ - дата рейса: ',
                    error_message='Дата вылета должна быть в формате ДД/ММ/ГГГГ!')

                validator(func=lambda x: len(x) == 5 and
                                         (x.replace(':', '').isdigit()),
                          input_message='ЧЧ:ММ - время вылета: ',
                          error_message='Время вылета должно быть в формате ЧЧ:ММ!')

                validator(
                    func=lambda x: x.replace('.', '').isdigit() and 0 < float(x) < 100,
                    input_message='XX.XX - длительность перелета: ',
                    error_message='Длительность полета должна быть в формате ЧЧ.ММ!')

                validator(
                    func=lambda x: len(x) == 3 and x.isalpha(),
                    input_message='XXX - аэропорт вылета: ',
                    error_message='Код ИАТА аэропорта вылета должен быть в формате XXX!')

                validator(
                    func=lambda x: len(x) == 3 and x.isalpha(),
                    input_message='XXX - аэропорт назначения: ',
                    error_message='Код ИАТА аэропорта прилёта должен быть в формате XXX!'
                )

                validator(func=lambda x: x.isdigit() and float(x) > 0,
                          input_message='.XX - стоимость билета (> 0): ',
                          error_message='Стоимость авиабилета должна быть больше 0!')

                print(
                    f'{print_cur_flight(flight_data=flight, number=flight_number)}* добавлена'
                )

            elif user_input == 2:
                print(print_flights())

            elif user_input == 3:
                user_flight_number: str = input('Введите номер рейса в формате XXXX: ')
                print(print_custom_flight(number=user_flight_number))

            else:
                print('Неизвестный пункт меню...')

        else:
            break


if __name__ == '__main__':
    start()
