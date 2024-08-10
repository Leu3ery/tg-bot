from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio
from aiogram import Bot, Dispatcher, types


#Не забути замінити 10с на 60с

class TrackingBot:
    def __init__(self, token: str, group_id , bd, user_bot=False):
        self.group_id = group_id
        self.bd = bd
        self.user_bot = user_bot
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.setup_handlers()


    def setup_handlers(self):
        @self.dp.chat_join_request()
        async def handle_chat_join_request(message: types.ChatJoinRequest):
            if (user := self.bd.get_user(user_id=message.from_user.id)) and user[0][4]:
                await self.bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
                print(f'User {message.from_user.id} was accepted')
            else:
                print(f'User {message.from_user.id} was rejected')
    


    async def periodic_task(self):
        while True:
            print('Periodic task')

            for user in self.bd.get_all_members():
                try:
                    if user[2] < datetime.now().strftime("%Y-%m-%d") and (await self.bot.get_chat_member(chat_id=self.group_id, user_id=user[1])).status == 'member':
                        await self.bot.ban_chat_member(chat_id=self.group_id, user_id=user[1])
                        await asyncio.sleep(0.5)
                        await self.bot.unban_chat_member(chat_id=self.group_id, user_id=user[1])
                        self.bd.del_member(user[1])
                        if self.user_bot != False:
                            try:
                                await self.user_bot.no_prime_message(user[1])
                            except: print(f'Не удалось написать {user[1]}')
                        print(f"User {user[1]} was kicked because of not having prime")
                except Exception as e:
                    print(e)
                    print(f'User {user[1]} not found')

            
            for user in self.bd.get_all_users():
                try:
                    # set prime on False if time of prime is over
                    if user[4] and (user[5] == None or user[5] < datetime.now().strftime("%Y-%m-%d")):
                        self.bd.set_have_prime(user[1], False)
                        self.bd.set_end_of_prime(user[1], None)
                except:
                    # Якщо користувач не є частиною чату або інша помилка
                    print(f"Error with user {user[1]}")

            await asyncio.sleep(10)  # Затримка 60 секунд


    async def run(self):
        asyncio.create_task(self.periodic_task())
        await self.dp.start_polling(self.bot)