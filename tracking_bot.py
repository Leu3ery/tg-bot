import os
import threading
import time
from dotenv import load_dotenv
import telebot
from telebot import types
from datetime import datetime, timedelta


load_dotenv()

#Не забути замінити 10с на 60с


class TrackingBot:
    def __init__(self, token, group_id, bd):
        self.group_id = group_id
        self.bot = telebot.TeleBot(token)
        self.bd = bd 
        self.setup_handlers()
        self.start_periodic_task()
        # self.start()


    def setup_handlers(self):
        # Declare handlers
        @self.bot.chat_join_request_handler()
        def handle_chat_join_request(message:types.ChatJoinRequest):
            if (user := self.bd.get_user(user_id=message.from_user.id)) and user[0][4]:
                # Try to accept the request
                try:
                    self.bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
                    print(f'User {message.from_user.id} was accepted')
                except:
                    print(f"User {message.from_user.id} was not accepted because of the error")
                # Try to send a message
                try:
                    # Надсилаємо повідомлення користувачу в особисті повідомлення
                    self.bot.send_message(chat_id=message.from_user.id, text="You have been accepted")
                except telebot.apihelper.ApiTelegramException as e:
                    if e.error_code == 403:
                        print(f"Failed to send message to {message.from_user.id}: Bot was blocked by the user")
                    else:
                        print(f"Failed to send message to {message.from_user.id}: {e}")
            else:
                print(f'User {message.from_user.id} was rejected')
    

    def start_periodic_task(self):
        def periodic_task():
            while True:
                # Your periodic task code here
                # print("Periodic task running...")
                for user in self.bd.get_all_users():
                    prime = user[4]
                    if user[4] and user[5] < datetime.now().strftime("%Y-%m-%d"):
                        self.bd.set_have_prime(user[1], False)
                        self.bd.set_end_of_prime(user[1], None)
                        prime = False  
                    user_status = self.bot.get_chat_member(chat_id=self.group_id, user_id=user[1]).status #left/member
                    # print(user_status, prime)
                    if user_status == 'member' and not prime:
                        self.bot.kick_chat_member(chat_id=self.group_id, user_id=user[1])
                        self.bot.unban_chat_member(chat_id=self.group_id, user_id=user[1])
                        print(f"User {user[1]} was kicked because of not having prime")
                time.sleep(10)  # 60 sec = 1 min

        # Create a separate thread for the periodic task
        task_thread = threading.Thread(target=periodic_task)
        task_thread.daemon = True  # The thread will be terminated when the main thread terminates
        task_thread.start()


    def start(self):
        print("Bot started")
        self.bot.infinity_polling()
        


if __name__ == "__main__":
    TRACKING_BOT_TOKEN = os.getenv('TRACKING_BOT_TOKEN') 
    GROUP_ID = os.getenv('GROUP_ID')

    import sql_helper
    bd = sql_helper.SqlHelper()

    my_bot = TrackingBot(TRACKING_BOT_TOKEN, GROUP_ID, bd)
    my_bot.start()