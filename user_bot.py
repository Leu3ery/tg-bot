import os
from dotenv import load_dotenv
import telebot
from telebot import types
import text_for_user_bot as Text


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
            Block(bot=self.bot, 
                  text=Text.block_start['text'], 
                  buttons=Text.block_start['buttons'],
                  edit=Text.block_start['edit']
                  ).place_block(message)
            
        @self.bot.callback_query_handler(func=lambda call: True)
        def answer(call):
            if 'menu' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_start['text'], 
                      buttons=Text.block_start['buttons'],
                      edit=True
                      ).place_block(call.message)
            elif call.data == 'channel':
                Block(bot=self.bot, 
                      text=Text.block_channel['text'], 
                      buttons=Text.block_channel['buttons'],
                      edit=Text.block_channel['edit']
                      ).place_block(call.message)
            elif call.data == 'choose_time':
                Block(bot=self.bot, 
                      text=Text.block_choose_time['text'], 
                      buttons=Text.block_choose_time['buttons'],
                      edit=Text.block_choose_time['edit']
                      ).place_block(call.message)
            elif call.data == 'question':
                Block(bot=self.bot,
                      text=Text.block_question['text'],
                      buttons=Text.block_question['buttons'],
                      edit=Text.block_question['edit']
                      ).place_block(call.message)
            elif 'time' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_choose_payment['text'], 
                      buttons=Text.block_choose_payment['buttons'],
                      edit=Text.block_choose_payment['edit'],
                      dop_callback='_'+call.data.split('_')[-1]
                      ).place_block(call.message)
            elif 'crypto' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_crypto['text']+'\n'+call.data.split('_')[-1], 
                      buttons=Text.block_crypto['buttons'],
                      edit=Text.block_crypto['edit']
                      ).place_block(call.message)
            elif 'lavatopusd' in call.data:
                Block(bot=self.bot, 
                      text=Text.block_lavatopusd['text']+'\n'+call.data.split('_')[-1], 
                      buttons=Text.block_lavatopusd['buttons'],
                      edit=Text.block_lavatopusd['edit']
                      ).place_block(call.message)

    def start(self):
        print("Bot started")
        self.bot.infinity_polling()
        


class Block:
    def __init__(self,bot:UserBot, text:str, buttons:list[tuple], edit:bool=False, dop_callback:str=""):
        self.bot = bot
        self.text = text
        self.buttons = buttons
        self.edit = edit
        self.dop_callback = dop_callback
    
    def place_block(self, message:types.Message):
        markup = types.InlineKeyboardMarkup()
        for text, callback_data in self.buttons:
            markup.add(types.InlineKeyboardButton(text=text, callback_data=callback_data+self.dop_callback))
        if self.edit:
            self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=self.text, reply_markup=markup)
        else:
            self.bot.send_message(chat_id=message.chat.id, text=self.text, reply_markup=markup)



if __name__ == "__main__":
    USER_BOT_TOKEN = os.getenv('USER_BOT_TOKEN')

    import sql_helper
    bd = sql_helper.SqlHelper()

    my_bot = UserBot(USER_BOT_TOKEN, bd)
    my_bot.start()