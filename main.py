import telebot
from telebot import types
import os
from dotenv import load_dotenv
from handlers import register_handler

load_dotenv()

token = os.getenv("BOT_API_TOKEN")

bot = telebot.TeleBot(token)

register_handler(bot)


# if __name__ == '__main__':
#     while True:
#         try:
#             bot.infinity_polling()
#         except Exception as e:
#             print("Сбой сервера телеграм-бота")


if __name__ == '__main__':
    bot.infinity_polling()
