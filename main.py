import os
from dotenv import load_dotenv
import sql_helper
import tracking_bot


load_dotenv()


bd = sql_helper.SqlHelper()

TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')
bot = tracking_bot.MyTeleBot(TRACKING_BOT_TOKEN, GROUP_ID, bd)
bot.start()