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
    new_message = "_Главное меню_"
    if not message_id:
        send_message(chatid, new_message, menu)
    else:
        send_message(chatid, new_message, menu)

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
