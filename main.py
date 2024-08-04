import os
from dotenv import load_dotenv
import sql_helper
import tracking_bot
import user_bot
import asyncio

load_dotenv()

async def main():
    # Ініціалізуємо базу даних
    bd = sql_helper.SqlHelper()

    # Отримуємо токени ботів і ідентифікатор групи
    TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN')
    GROUP_ID = os.getenv('GROUP_ID')
    USER_BOT_TOKEN = os.getenv('USER_BOT_TOKEN')

    # Створюємо екземпляри ботів
    for_users_bot = user_bot.UserBot(USER_BOT_TOKEN, bd)
    in_group_bot = tracking_bot.TrackingBot(TRACKING_BOT_TOKEN, GROUP_ID, bd, for_users_bot)

    await asyncio.gather(
        for_users_bot.run(),
        in_group_bot.run()
    )

if __name__ == "__main__":
    asyncio.run(main())