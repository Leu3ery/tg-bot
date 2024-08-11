import os
from dotenv import load_dotenv
import sql_helper
import tracking_bot
import user_bot
import asyncio
import lavatop_api as Lava
import crypto as Crypto

load_dotenv()

async def main():
    # Ініціалізуємо базу даних
    bd = sql_helper.SqlHelper()

    # Отримуємо токени ботів і ідентифікатор групи
    TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN')
    GROUP_ID = os.getenv('GROUP_ID')
    USER_BOT_TOKEN = os.getenv('USER_BOT_TOKEN')
    CHANEL_LINK = os.getenv('CHANEL_LINK')
    LAVATOP_API = os.getenv('LAVATOP_API')
    CRYPTO_ADRESS = os.getenv('CRYPTO_TOKEN')

    USER_BOT = os.getenv('USER_BOT')

    for_users_bot = user_bot.UserBot(USER_BOT_TOKEN, bd, link_on_chanel=CHANEL_LINK, lavatop_api=Lava.LavaTopAPI(LAVATOP_API), crypto_api=Crypto.CryptoApi(CRYPTO_ADRESS))
    in_group_bot = tracking_bot.TrackingBot(TRACKING_BOT_TOKEN, GROUP_ID, bd, for_users_bot if USER_BOT == 'True' else False)

    await asyncio.gather(
        for_users_bot.run(),
        in_group_bot.run()
    )

if __name__ == "__main__":
    asyncio.run(main())