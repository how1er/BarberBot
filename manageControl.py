import telebot
from telebot import types
from db import Barber_list_price

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
    for BarberName, Price in barbers:
        barbers_list_message += str(BarberName) + ": " + str(Price) + "р." + "\n"
    if not message_id:
        send_message(chatid, barbers_list_message, menu)
    else:
        edit_message(chatid, message_id, barbers_list_message,menu,  markdown=True)

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
    for BarberName, Price in barbers:
        menu.add(types.InlineKeyboardButton(text=str(BarberName), callback_data=str(BarberName)))
    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='to_main_menu'))
    if not message_id:
        send_message(chatid, select_barber_message, menu)
    else:
        edit_message(chatid, message_id, select_barber_message,menu,  markdown=True)


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
