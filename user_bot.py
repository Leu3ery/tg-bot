import os
import time
from dotenv import load_dotenv
import telebot
from telebot import types
import text_for_user_bot as Text
from datetime import datetime, timedelta


#Не забути замітити minutes на hours

load_dotenv()


class UserBot:
    def __init__(self, token, bd):
        self.bot = telebot.TeleBot(token)
        self.bd = bd 
        self.setup_handlers()
        # self.start()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bd.add_new_user(message.chat.id)
            self.bd.set_start_of_using_bot(message.chat.id, datetime.now().strftime("%Y-%m-%d"))
            Block(bot=self.bot, 
                  text=Text.block_start['text'], 
                  buttons=Text.block_start['buttons'],
                  edit=Text.block_start['edit'],
                  bd=self.bd
                  ).place_block(message)
        

        @self.bot.message_handler(commands=['noprime'])
        def no_prime(message):
            self.bd.set_have_prime(message.chat.id, False)
            self.bd.set_end_of_prime(message.chat.id, None)
            Block(bot=self.bot,
                  text='Tи потерял доступ к каналу. Хотите снова получить?',
                  buttons=[('Да', 'choose_time'), ('Нет', 'menu')],
                  edit=False,
                  bd=self.bd,
                  anyway=True
                  ).place_block(message)
        
        @self.bot.message_handler(commands=['notimer'])
        def no_prime(message):
            self.bd.set_end_of_timer(message.chat.id, None)
            self.bot.send_message(chat_id=message.chat.id, text='Появилось окно оплати. Жми /start')

            
        @self.bot.callback_query_handler(func=lambda call: True)
        def answer(call):
            if 'menu' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_start['text'], 
                      buttons=Text.block_start['buttons'],
                      edit=True,
                      bd=self.bd
                      ).place_block(call.message)
            elif call.data == 'channel':
                Block(bot=self.bot, 
                      text=Text.block_channel['text'], 
                      buttons=Text.block_channel['buttons'],
                      edit=Text.block_channel['edit'],
                      bd=self.bd
                      ).place_block(call.message)
            elif call.data == 'choose_time':
                self.set_timer(call.message.chat.id)
                Block(bot=self.bot, 
                      text=Text.block_choose_time['text'], 
                      buttons=Text.block_choose_time['buttons'],
                      edit=Text.block_choose_time['edit'],
                      bd=self.bd
                      ).place_block(call.message)
            elif call.data == 'question':
                Block(bot=self.bot,
                      text=Text.block_question['text'],
                      buttons=Text.block_question['buttons'],
                      edit=Text.block_question['edit'],
                      bd=self.bd
                      ).place_block(call.message)
            elif 'time' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_choose_payment['text'], 
                      buttons=Text.block_choose_payment['buttons'],
                      edit=Text.block_choose_payment['edit'],
                      dop_callback='_'+call.data.split('_')[-1],
                      bd=self.bd
                      ).place_block(call.message)
            elif 'crypto' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_crypto['text']+'\n'+call.data.split('_')[-1], 
                      buttons=Text.block_crypto['buttons'],
                      edit=Text.block_crypto['edit'],
                      dop_callback='_'+call.data.split('_')[-1],
                      bd=self.bd
                      ).place_block(call.message)
            elif 'lavatopusd' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_lavatopusd['text']+'\n'+call.data.split('_')[-1], 
                      buttons=Text.block_lavatopusd['buttons'],
                      edit=Text.block_lavatopusd['edit'],
                      dop_callback='_'+call.data.split('_')[-1],
                      bd=self.bd
                      ).place_block(call.message)
            elif 'for_free' in call.data:
                self.bd.set_have_prime(call.message.chat.id, True)
                self.bd.set_end_of_prime(call.message.chat.id, (datetime.now() + timedelta(days=30*int(a) if (a:=call.data.split('_')[-1]) != 'forever' else 9999)).strftime("%Y-%m-%d"))
                Block(bot=self.bot, 
                      text='Ты получил доступ к каналу: \nhttps://t.me/+mtojuZOTFE4zMTIy', 
                      buttons=[('В меню', 'menu')],
                      edit=True,
                      bd=self.bd
                      ).place_block(call.message)
    
    def set_timer(self, user_id, anyway=False):
        if self.bd.get_user(user_id)[0][7] == None or anyway:
            self.bd.set_end_of_timer(user_id, datetime.now() + timedelta(minutes=Text.timer_settings['how_long']))
            self.bot.send_message(chat_id=user_id, text=f'Доступ к боту закроется в {datetime.strptime(self.bd.get_user(user_id)[0][7], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M")}')

    def start(self):
        print("Bot started")
        self.bot.infinity_polling()
        


class Block:
    def __init__(self,bot:UserBot, text:str, buttons:list[tuple], bd, edit:bool=False, dop_callback:str="", anyway:bool=False):
        self.bd = bd
        self.bot = bot
        self.text = text
        self.buttons = buttons
        self.edit = edit
        self.dop_callback = dop_callback
        self.anyway = anyway
    
    def place_block(self, message:types.Message):
        if (timer := self.bd.get_user(message.chat.id)[0][7]) == None or datetime.strptime(timer, "%Y-%m-%d %H:%M:%S.%f") > datetime.now() or self.anyway:
            markup = types.InlineKeyboardMarkup()
            for text, callback_data in self.buttons:
                markup.add(types.InlineKeyboardButton(text=text, callback_data=callback_data+self.dop_callback))
            if self.edit:
                self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=self.text, reply_markup=markup)
            else:
                self.bot.send_message(chat_id=message.chat.id, text=self.text, reply_markup=markup)
        else:
            if self.edit:
                self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Твое время вышло. Включи уведомления чтоби успеть в следующий раз...')
            else:
                self.bot.send_message(chat_id=message.chat.id, text='Твое время вышло. Включи уведомления чтоби успеть в следующий раз...')



if __name__ == "__main__":
    USER_BOT_TOKEN = os.getenv('USER_BOT_TOKEN')

    import sql_helper
    bd = sql_helper.SqlHelper()

    my_bot = UserBot(USER_BOT_TOKEN, bd)
    my_bot.start()