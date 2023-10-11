# MyProfile app

SEPARATOR = '------------------------------------------'

# user profile
name = ''
age = 0
phone = ''
email = ''
index = ''
p_index = ''
inf = ''
# BUSINESS
ogrnip = ''
inn = ''
payment_acc = ''
bank_name = ''
bik = ''
corresp_acc = ''


def general_info_user(name_parameter, age_parameter, phone_parameter, email_parameter, index_parameter,
                      p_index_parameter, inf_parameter):
    print(SEPARATOR)
    print('Имя:       ', name_parameter)
    if 11 <= age_parameter % 100 <= 19:
        years_parameter = 'лет'
    elif age_parameter % 10 == 1:
        years_parameter = 'год'
    elif 2 <= age_parameter % 10 <= 4:
        years_parameter = 'года'
    else:
        years_parameter = 'лет'

    new_index = ''
    for n_s in index_parameter:
        if n_s == "1" or n_s == "2" or n_s == "3" or n_s == "4" or n_s == "5" or n_s == "6" \
                or n_s == "7" or n_s == "8" or n_s == "9" or n_s == "0":
            new_index += n_s
    index_parameter = new_index

    print('Возраст:   ', age_parameter, years_parameter)
    print('Телефон:   ', phone_parameter)
    print('E-mail:    ', email_parameter)
    print('Индекс:    ', index_parameter)
    print('Адрес:     ', p_index_parameter)
    print()
    if inf:
        print('\nДополнительная информация:')
        print(inf_parameter)


print('Приложение MyProfile для предпринимателей')
print('Сохраняй информацию о себе и выводи ее в разных форматах')

while True:
    # main menu
    print(SEPARATOR)
    print('ГЛАВНОЕ МЕНЮ')
    print('1 - Ввести или обновить информацию')
    print('2 - Вывести информацию')
    print('0 - Завершить работу')

    option = int(input('Введите номер пункта меню: '))
    if option == 0:
        break

    if option == 1:
        # submenu 1: edit info
        while True:
            print(SEPARATOR)
            print('ВВЕСТИ ИЛИ ОБНОВИТЬ ИНФОРМАЦИЮ')
            print('1 - Личная информация')
            print('2 - Информация о предпринимателе')
            print('0 - Назад')

            option2 = int(input('Введите номер пункта меню: '))
            if option2 == 0:
                break
            if option2 == 1:
                # input general info
                name = input('Введите имя: ')
                while 1:
                    # validate user age
                    age = int(input('Введите возраст: '))
                    if age > 0:
                        break
                    print('Возраст должен быть положительным')

                uphone = input('Введите номер телефона (+7ХХХХХХХХХХ): ')
                phone = ''
                for sym in uphone:
                    if sym == '+' or ('0' <= sym <= '9'):
                        phone += sym

                email = input('Введите адрес электронной почты: ')
                index = input('Введите почтовый индекс: ')
                p_index = input('Введите почтовый адрес (без индекса): ')
                inf = input('Введите дополнительную информацию:\n')

            elif option2 == 2:
                # BUSINESS
                while 1:
                    uogrnip = int(input('Введите ОГРНИП: '))
                    new_ogrnip = uogrnip
                    count1 = 0
                    while uogrnip > 0:
                        count1 += 1
                        uogrnip //= 10
                    if count1 >= 15:
                        ogrnip = new_ogrnip
                        break
                    print('ОГРНИП должен содержать 15 цифр')

                inn = int(input('Введите ИНН: '))

                while 1:
                    upayment = int(input('Введите расчетный счет: '))
                    count2 = 0
                    new_payment = upayment
                    while upayment > 0:
                        count2 += 1
                        upayment //= 10
                    if count2 >= 20:
                        payment_acc = new_payment
                        break
                    print('Расчетный счет должен содержать 20 цифр')

                bank_name = input('Введите название банка: ')
                bik = int(input('Введите БИК: '))
                corresp_acc = int(input('Введите корреспондентский счет: '))
            else:
                print('Введите корректный пункт меню')
    elif option == 2:
        # submenu 2: print info
        while True:
            print(SEPARATOR)
            print('ВЫВЕСТИ ИНФОРМАЦИЮ')
            print('1 - Общая информация')
            print('2 - Вся информация')
            print('0 - Назад')

            option2 = int(input('Введите номер пункта меню: '))
            if option2 == 0:
                break
            if option2 == 1:
                general_info_user(name, age, phone, email, index, p_index, inf)

            elif option2 == 2:
                general_info_user(name, age, phone, email, index, p_index, inf)

                # print BUSINESS
                print('Информация о предпринимателе')
                print('ОГРНИП:   ', ogrnip)
                print('ИНН:      ', inn)
                print('Банковские реквизиты')
                print('Р/с:      ', payment_acc)
                print('Банк:     ', bank_name)
                print('БИК:      ', bik)
                print('К/с:      ', corresp_acc)
            else:
                print('Введите корректный пункт меню')
    else:
        print('Введите корректный пункт меню')
