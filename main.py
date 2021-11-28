import telebot
import sqlite3
from aiogram import types
from db import dbstart

bot = telebot.TeleBot('2120063146:AAGFdvPdx22l_DvrW4xejLaM7YUNvQwbyAc')


@bot.message_handler(commands=['start'])
def start_messages(message):
    chatid = message.chat.id
    bot.send_message(message.from_user.id, "Привет, напиши свое имя")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, " + message.text)


if __name__ == '__main__':
    dbstart()
    bot.polling(none_stop=True, interval=0)
