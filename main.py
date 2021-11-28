import telebot
import sqlite3
from aiogram import types
from db import dbstart, check_new_client, Barber_list_price
from manageControl import new_user

bot = telebot.TeleBot('2120063146:AAGFdvPdx22l_DvrW4xejLaM7YUNvQwbyAc')


@bot.message_handler(commands=['start'])
def start_messages(message):
    chatid = message.chat.id
    if check_new_client(chatid):
        new_user(chatid)
        # bot.send_message(message.from_user.id, "Добро пожаловать в BarberBot, напиши свое имя")
    else:
        bot.send_message(message.from_user.id, "Привет, похоже ты тут уже был")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, " + message.text)


@bot.callback_query_handler(func=lambda message: True)
def answer(message):
    if message.data == 'price_list':
        try:
            barbers = Barber_list_price()
            barbers_list_message = ""
            for BarberName, Price in barbers:
                barbers_list_message += str(BarberName) + ' ' + str(Price) + "\n"
            bot.send_message(message.from_user.id, barbers_list_message)
        except Exception as e:
            print(message.data + ' Error: ', e)


if __name__ == '__main__':
    dbstart()
    bot.polling(none_stop=True, interval=0)
