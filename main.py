import datetime

import telebot
import sqlite3
from aiogram import types
from db import dbstart, isNewClient, Barber_list_price, columnLists, barberFreeTime
from manageControl import new_user, mainmenu, barber_list, select_barber, select_day, select_time, new_order, waiting, \
    set_mark, add_mark_to_db, history_menu

bot = telebot.TeleBot('2120063146:AAGFdvPdx22l_DvrW4xejLaM7YUNvQwbyAc')


@bot.message_handler(commands=['start'])
def start_messages(message):
    chatid = message.chat.id
    if isNewClient(chatid):
        new_user(chatid)
        # bot.send_message(message.from_user.id, "Добро пожаловать в BarberBot, напиши свое имя")
    else:
        mainmenu(chatid)
        # bot.send_message(message.from_user.id, "Привет, похоже ты тут уже был")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, " + message.text)


@bot.callback_query_handler(func=lambda message: True)
def answer(message):
    chatid = message.message.chat.id
    barber_id = None
    time = None
    if message.data == 'price_list':
        try:
            barber_list(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'to_main_menu':
        try:
            mainmenu(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'back_to_welcome':
        try:
            new_user(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif message.data == 'new_haircut':
        try:
            select_barber(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif 'barber_' in message.data:
        try:
            barber_id = message.data[-1]
            select_day(chatid, message.message.message_id, barber_id)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif 'date_' in message.data:
        try:
            message_copy = message.data
            info_str = message_copy.replace("_date_", "_")
            select_time(chatid, message.message.message_id, info_str)
            print(info_str)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif 'time_' in message.data:
        try:
            message_copy = message.data
            info_str = message_copy.replace("_time_", " ")
            print(info_str)
            new_order(chatid, message.message.message_id, info_str)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif 'to_waiting' in message.data:
        try:
            message_copy = message.data
            info_str = message_copy.replace("to_waiting_", "")
            waiting(chatid, message.message.message_id, info_str)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif 'to_mark' in message.data:
        try:
            message_copy = message.data
            info_str = message_copy.replace("to_mark_", "")
            set_mark(chatid, message.message.message_id, info_str)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif '_marked_' in message.data:
        try:
            message_copy = message.data
            info_str = message_copy.replace("_marked_", "_")
            add_mark_to_db(chatid, message.message.message_id, info_str)
        except Exception as e:
            print(message.data + ' Error: ', e)
    elif 'history' in message.data:
        try:
            history_menu(chatid, message.message.message_id)
        except Exception as e:
            print(message.data + ' Error: ', e)


if __name__ == '__main__':
    dbstart()
    #columnLists('Barbers')
    #barberFreeTime(1, datetime.datetime.today())
    bot.polling(none_stop=True, interval=0)
