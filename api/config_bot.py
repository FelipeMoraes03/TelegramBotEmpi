import telebot
from dotenv import dotenv_values

# Initialize telegram bot
config = dotenv_values(".env")
bot = telebot.TeleBot(config['TELEGRAM_API_KEY'])