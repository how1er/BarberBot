import telebot
from telebot import types

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


def main_menu(chatid, message_id=False):
    pass

def new_user(chatid):
    """
    Меню для нового пользователя
    :param chatid: id пользователя
    :return:
    """
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='Прайс-лист', callback_data='price_list'))
    menu.add(types.InlineKeyboardButton(text="Инструкция по сервису", callback_data='instructions'))
    menu.add(types.InlineKeyboardButton(text="Продолжить", callback_data='to_main_menu'))
    welcome_message = "Добро пожаловать в BarberBot!"
    send_message(chatid, welcome_message, menu)
