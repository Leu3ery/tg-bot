import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN')

bot = telebot.TeleBot(TRACKING_BOT_TOKEN)

# Хендлер для обробки запитів на вступ до каналу
@bot.chat_join_request_handler()
def handle_chat_join_request(message:types.ChatJoinRequest):
    # Приймаємо користувача в канал (ця функція автоматично схвалює запити на вступ)
    bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
    # Надсилаємо повідомлення користувачу в особисті повідомлення
    bot.send_message(chat_id=message.from_user.id, text="текст сообщения бота в лс юзеру")

# Запуск бота
bot.polling(none_stop=True)
