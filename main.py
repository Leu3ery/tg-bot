# import os
# from dotenv import load_dotenv
# import sql_helper
# import tracking_bot
# import user_bot


# load_dotenv()


# bd = sql_helper.SqlHelper()

# TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN')
# GROUP_ID = os.getenv('GROUP_ID')
# in_group_bot = tracking_bot.TrackingBot(TRACKING_BOT_TOKEN, GROUP_ID, bd)
# in_group_bot.start()

# USER_BOT_TOKEN = os.getenv('USER_BOT_TOKEN')
# for_users_bot = user_bot.UserBot(USER_BOT_TOKEN, bd)
# for_users_bot.start()

import os
import threading
from dotenv import load_dotenv
import sql_helper
import tracking_bot
import user_bot

load_dotenv()

# Ініціалізуємо базу даних
bd = sql_helper.SqlHelper()

# Отримуємо токени ботів і ідентифікатор групи
TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')
USER_BOT_TOKEN = os.getenv('USER_BOT_TOKEN')

# Створюємо екземпляри ботів
in_group_bot = tracking_bot.TrackingBot(TRACKING_BOT_TOKEN, GROUP_ID, bd)
for_users_bot = user_bot.UserBot(USER_BOT_TOKEN, bd)

def start_tracking_bot():
    in_group_bot.start()

def start_user_bot():
    for_users_bot.start()

# Створюємо та запускаємо потоки
tracking_bot_thread = threading.Thread(target=start_tracking_bot)
user_bot_thread = threading.Thread(target=start_user_bot)

# Робимо потоки демонстраційними, щоб вони завершились разом з основним потоком
tracking_bot_thread.daemon = True
user_bot_thread.daemon = True

tracking_bot_thread.start()
user_bot_thread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Main thread interrupted. Exiting...")