import telebot
import datetime
from telebot import types
from db import Barber_list_price, barberFreeTime, takeOrder, columnLists, isFreeOrder, update_mark, History

bot = telebot.TeleBot('2120063146:AAGFdvPdx22l_DvrW4xejLaM7YUNvQwbyAc')


def send_message(chatid, welcome_message, menu=None, markdown=True):
    """
    Отправка нового сообщения
    :param chatid: id пользователя, которому нужно отправить
    :param welcome_message: текст сообщения
    :param menu: меню сообщения
    :param markdown: включение или отключение разметки
    :return: при успешной отправке True, иначе False
    """
    try:
        if not menu:
            bot.send_message(chatid, welcome_message, parse_mode='Markdown')
        else:
            if markdown:
                bot.send_message(chatid, welcome_message, reply_markup=menu, parse_mode='Markdown')
            else:
                bot.send_message(chatid, welcome_message, reply_markup=menu)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def edit_message(chatid, messageid, new_message, menu=None, markdown=True):
    """
    Редактирование существующего сообщения
    :param chatid: id пользователя, которому нужно отправить
    :param messageid: id сообщения
    :param new_message: текст нового сообщения
    :param menu: меню нового сообщения
    :param markdown: включение или отключение разметки
    :return: при успешном редактировании True, иначе False
    """
    try:
        if not menu:
            bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, parse_mode='Markdown')
        else:
            if markdown:
                bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, reply_markup=menu,
                                      parse_mode='Markdown')
            else:
                bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, reply_markup=menu)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def mainmenu(chatid, message_id=False):
    """
    Формирование и отправка главного меню.
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :return:
    """
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='✂Записаться на стрижку', callback_data='new_haircut'))
    menu.add(types.InlineKeyboardButton(text='🗒История', callback_data='history'))
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='back_to_welcome'))
    new_message = "_Главное меню_"
    if not message_id:
        send_message(chatid, new_message, menu)
    else:
        edit_message(chatid, message_id, new_message, menu, markdown=True)


def barber_list(chatid, message_id=False):
    """
    Список барберов с прайсом.
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Прайс-лист (средняя цена)', callback_data='price_list'))
    menu.add(types.InlineKeyboardButton(text="Инструкция по сервису", callback_data='instructions'))
    menu.add(types.InlineKeyboardButton(text="Продолжить", callback_data='to_main_menu'))
    barbers = Barber_list_price()
    barbers_list_message = ""
    for barberId, BarberName, Price in barbers:
        barbers_list_message += str(BarberName) + ": " + str(Price) + "р." + "\n"
    if not message_id:
        send_message(chatid, barbers_list_message, menu)
    else:
        edit_message(chatid, message_id, barbers_list_message, menu, markdown=True)


def select_barber(chatid, message_id=False):
    """
    Список барберов (кнопки).
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    barbers = Barber_list_price()
    select_barber_message = "Выберете барбера"
    for barberId, BarberName, Price in barbers:
        menu.add(types.InlineKeyboardButton(text=str(BarberName), callback_data='barber_' + str(barberId)))
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='to_main_menu'))
    if not message_id:
        send_message(chatid, select_barber_message, menu)
    else:
        edit_message(chatid, message_id, select_barber_message, menu, markdown=True)


def select_day(chatid, message_id=False, barber=""):
    """
    Выбор дня.
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :param barber: Идентификатор барбера
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    barberid = barber[-1]
    date = datetime.datetime.today()
    select_time_message = "Выберете день для записи"
    for i in range(7):
        menu.add(types.InlineKeyboardButton(text=str(date.date().strftime('%d/%m')),
                                            callback_data=barberid + "_date_" + date.strftime('%Y-%m-%d')))
        date += datetime.timedelta(days=1)
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='new_haircut'))
    if not message_id:
        send_message(chatid, select_time_message, menu)
    else:
        edit_message(chatid, message_id, select_time_message, menu, markdown=True)


def select_time(chatid, message_id=False, info=""):
    """
    Список свободного времени (кнопки).
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :param info: Идентификатор барбера и дата
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    barberid = int(info[0])
    date = datetime.datetime.strptime(info.split('_')[1], '%Y-%m-%d')
    time = barberFreeTime(barberid, date)
    select_time_message = "Выберете свободное время"
    for order_time in time:
        dt_value = datetime.datetime.strptime(order_time[0], '%Y-%m-%d %H:%M:%S')
        menu.add(types.InlineKeyboardButton(text=str(dt_value.time().strftime('%H:%M')),
                                            callback_data=info + "_time_" + dt_value.strftime('%H:%M:%S')))
    menu.add(types.InlineKeyboardButton(text='К выбору дня', callback_data='barber_' + str(barberid)))
    if not message_id:
        send_message(chatid, select_time_message, menu)
    else:
        edit_message(chatid, message_id, select_time_message, menu, markdown=True)


def new_order(chatid, message_id=False, info=""):
    """
    Формирование нового заказа.
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :param info: Идентификатор барбера и время
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    barberid = int(info.split('_')[0])
    time = datetime.datetime.strptime(info.split('_')[1], '%Y-%m-%d %H:%M:%S')
    ord_id = takeOrder(chatid, time, barberid)
    print(ord_id)
    new_order_message = "Бронь зарегистрирована"
    menu.add(types.InlineKeyboardButton(text='Далее', callback_data='to_waiting_' + str(ord_id)))
    if not message_id:
        send_message(chatid, new_order_message, menu)
    else:
        edit_message(chatid, message_id, new_order_message, menu, markdown=True)


def waiting(chatid, message_id=False, info=""):
    """
    Ожидание конца стрижки.
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :param info: Идентификатор заказа
    :return:
    """

    orderid = int(info.split('_')[0])
    menu = types.InlineKeyboardMarkup()
    new_order_message = "Стрижка завершена?"
    menu.add(types.InlineKeyboardButton(text='Да', callback_data='to_mark_' + str(orderid)))
    menu.add(types.InlineKeyboardButton(text='Нет', callback_data='to_waiting_' + str(orderid)))
    if not message_id:
        send_message(chatid, new_order_message, menu)
    else:
        edit_message(chatid, message_id, new_order_message, menu, markdown=True)


def set_mark(chatid, message_id=False, info=""):
    """
    Простановка оценки.
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :param info: Идентификатор барбера
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    orderid = int(info.split('_')[0])
    new_order_message = "Поставьте оценку от 1 до 5"
    for i in range(5):
        menu.add(types.InlineKeyboardButton(text=str(i + 1), callback_data=str(orderid) + '_marked_' + str(i + 1)))
    if not message_id:
        send_message(chatid, new_order_message, menu)
    else:
        edit_message(chatid, message_id, new_order_message, menu, markdown=True)


def add_mark_to_db(chatid, message_id=False, info=""):
    """
    Простановка оценки в бд
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :param info: Идентификатор заказа и оценка
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    orderid = int(info.split('_')[0])
    mark = int(info.split('_')[1])
    update_mark(orderid, mark)
    columnLists('Orders')
    add_mark_to_db = "Спасибо вам за стрижку. Будем ждать вас снова."
    menu.add(types.InlineKeyboardButton(text="К главному меню", callback_data='to_main_menu'))
    if not message_id:
        send_message(chatid, add_mark_to_db, menu)
    else:
        edit_message(chatid, message_id, add_mark_to_db, menu, markdown=True)


def history_menu(chatid, message_id=False):
    """
    Вывод истории заказов
    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :return:
    """

    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text="К главному меню", callback_data='to_main_menu'))
    history_list = History(chatid)
    history_list_message = ""
    if len(history_list) != 0:
        for barberName, order_time, rating in history_list:
            history_list_message += "Барбер: " + str(barberName) + ", время: " + str(order_time) + ", оценка: " \
                                    + str(rating) + "\n"
    else:
        history_list_message = "У вас еще не было стрижек"
    if not message_id:
        send_message(chatid, history_list_message, menu)
    else:
        edit_message(chatid, message_id, history_list_message, menu, markdown=True)


def new_user(chatid, message_id=False):
    """
    Меню для нового пользователя
    :param chatid: id пользователя
    :return:
    """
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Прайс-лист', callback_data='price_list'))
    menu.add(types.InlineKeyboardButton(text="Инструкция по сервису", callback_data='instructions'))
    menu.add(types.InlineKeyboardButton(text="Продолжить", callback_data='to_main_menu'))
    welcome_message = "_Добро пожаловать в BarberBot!_"
    if not message_id:
        send_message(chatid, welcome_message, menu)
    else:
        edit_message(chatid, message_id, welcome_message, menu, markdown=True)
