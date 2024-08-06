import text_for_user_bot_copy as Text
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



class UserBot:
    def __init__(self, token: str, bd, link_on_chanel:str):
        USER_BOT = os.getenv('USER_BOT')
        if USER_BOT == 'True':
            self.bd = bd
            self.bot = Bot(token=token)
            self.dp = Dispatcher()
            self.link_on_chanel = link_on_chanel
            self.callback_handler = CallbackHandler(self.bot, self.bd, self.set_timer, self.update_dop_text_file, self.link_on_chanel)
            self.message_handler = MessageHandler(self.bot, self.callback_handler)
            self.setup_handlers()
        else:
            print('USER_BOT = False')


    def setup_handlers(self):
        @self.dp.message(CommandStart())
        async def on_start(message: types.Message):
            self.bd.add_new_user(message.chat.id)
            self.bd.set_start_of_using_bot(message.chat.id, datetime.now().strftime("%Y-%m-%d"))
            self.bd.set_nickname(message.chat.id, message.chat.username)
            if self.bd.get_user(message.chat.id)[0][8] == 1 and self.bd.get_user(message.chat.id)[0][7] != None:
                self.bd.set_end_of_timer(message.chat.id, None)
            if (timer := self.bd.get_user(message.chat.id)[0][7]) == None or datetime.strptime(timer, "%Y-%m-%d %H:%M:%S.%f") > datetime.now():
                buttons = [[InlineKeyboardButton(text=button_text, callback_data=call)] for button_text, call in Text.block_start['buttons']]
                markup = InlineKeyboardMarkup(inline_keyboard=buttons)
                await message.answer(Text.block_start['text'], reply_markup=markup)
                if (timer := self.bd.get_user(message.chat.id)[0][7]) != None:
                    await self.bot.send_message(chat_id=message.chat.id, text=f'{Text.timer_settings['end_of_timer_text']} {datetime.strptime(self.bd.get_user(message.chat.id)[0][7], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M")}')
            else:
                await message.answer(Text.timer_settings['timer_is_over_text'])
        
        @self.dp.message(Command('admin'))
        async def admin(message: types.Message):
            self.bd.add_new_user(message.chat.id)
            self.bd.set_start_of_using_bot(message.chat.id, datetime.now().strftime("%Y-%m-%d"))
            self.bd.set_nickname(message.chat.id, message.chat.username)
            buttons = [[InlineKeyboardButton(text=button_text, callback_data=call)] for button_text, call in Text.block_admin['buttons']]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer(Text.block_admin['text'], reply_markup=markup)
        
        @self.dp.message(Command('noprime'))
        async def on_noprime(message: types.Message):
            #ASYNC
            self.bd.set_have_prime(message.chat.id, False)
            self.bd.set_end_of_prime(message.chat.id, None)

        @self.dp.message(Command('notimer'))
        async def on_notimer(message: types.Message):
            self.bd.set_end_of_timer(message.chat.id, None)
            await self.bot.send_message(chat_id=message.chat.id, text=Text.timer_settings['new_timer_text'])
        
        @self.dp.callback_query(lambda c: c.data)
        async def process_callback(call: types.CallbackQuery):
            await self.callback_handler.handle(call)
        
        @self.dp.message()
        async def on_message(message: types.Message):
            await self.message_handler.handle(message)
            
    
    async def no_prime_message(self, user_id):
        buttons = [[InlineKeyboardButton(text=button_text, callback_data=call)] for button_text, call in Text.block_noprime['buttons']]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await self.bot.send_message(chat_id=user_id, text=Text.block_noprime['text'], reply_markup=markup)
    
    async def set_timer(self, user_id, dop_time=0):
        if self.bd.get_user(user_id)[0][7] == None and self.bd.get_user(user_id)[0][8] == 0:
            self.bd.set_end_of_timer(user_id, datetime.now() + timedelta(minutes=Text.timer_settings['how_long']))
        if dop_time != 0:
            self.bd.set_end_of_timer(user_id, datetime.now() + timedelta(minutes=dop_time))
        await self.bot.send_message(chat_id=user_id, text=f'{Text.timer_settings['end_of_timer_text']} {datetime.strptime(self.bd.get_user(user_id)[0][7], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M")}')

    async def update_dop_text_file(self):
        # Формуємо рядок з вмістом для запису
        content = f"""timer_settings = {Text.timer_settings}
block_noprime = {Text.block_noprime}
block_start = {Text.block_start}
block_channel = {Text.block_channel}
block_question = {Text.block_question}
block_choose_time = {Text.block_choose_time}
block_choose_payment = {Text.block_choose_payment}
block_crypto = {Text.block_crypto}
block_lavatopusd = {Text.block_lavatopusd}
block_got_access = {Text.block_got_access}
block_admin = {Text.block_admin}
block_myPrime = {Text.block_myPrime}

buttons_list = {Text.buttons_list}

dop = {{
    'block_start': block_start,
    'block_channel': block_channel,
    'block_question': block_question,
    'block_choose_time': block_choose_time,
    'block_choose_payment': block_choose_payment,
    'block_crypto': block_crypto,
    'block_lavatopusd': block_lavatopusd,
    'block_got_access': block_got_access,
    'block_noprime': block_noprime,
    'timer_settings': timer_settings,
    'block_admin': block_admin,
    'block_myPrime': block_myPrime
}}
    """

        # Записуємо вміст у файл dop_text.py
        with open('text_for_user_bot_copy.py', 'w', encoding='utf-8') as f:
            f.write(content)
                
    async def run(self):
        print('Bot started')
        await self.dp.start_polling(self.bot)


class CallbackHandler:
    def __init__(self, bot, bd, set_timer, update_dop_text_file, link_on_chanel):
        self.bot = bot
        self.bd = bd
        self.set_timer = set_timer
        self.update_dop_text_file = update_dop_text_file
        self.link_on_chanel = link_on_chanel

        self.temp_text = ''
        self.block_text_edit = ''
        self.block_button_edit = ''
        self.block_button_num_edit = ''

        self.send_message = False
        self.send_photo = False
        self.temp_photo = None

        self.admin_timer_change_time = False
        self.admin_timer_restart = False
        self.admin_timer_text_timerOver = False
        self.admin_timer_close = False
        self.admin_timer_paymentStart = False

    async def admin_block(self, call):
        if call.data == 'admin_block':
            self.temp_text = ''
            self.block_text_edit = ''
            self.block_button_edit = ''
            self.block_button_num_edit = ''
            await Block(text="Ти в разделе изменения блоков", 
            buttons=[('Стартовый блок', 'admin_block_start'), ('Канал', 'admin_block_channel'), ('Вопросы', 'admin_block_question'), ('Подписки', 'admin_block_myPrime'), ('Выбор времени', 'admin_block_choose_time'), ('Выбор способа оплаты', 'admin_block_choose_payment'), ('Криптовалюта', 'admin_block_crypto'), ('Лаватоп', 'admin_block_lavatopusd'), ('При получении доступа', 'admin_block_got_access'), ('При окончании премиума', 'admin_block_noprime'), ('В админ меню', 'admin_menu')],
            edit=True,
            bd=self.bd,
            anyway=True
            ).place_block(call)
        elif call.data == 'admin_block_text_change':
            block_name = self.block_text_edit
            Text.dop[block_name]['text'] = self.temp_text
            await self.update_dop_text_file()
            self.temp_text = ''
            self.block_text_edit = ''
            await Block(text='Текст изменен',
                  buttons=[('<- Назад', f'admin_{block_name}'), ('В админ меню', 'admin_menu')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
        elif call.data == 'admin_block_button_change':
            block_name = self.block_button_edit
            Text.dop[block_name]['buttons'][int(self.block_button_num_edit)] = (self.temp_text, Text.dop[block_name]['buttons'][int(self.block_button_num_edit)][1])
            await self.update_dop_text_file()
            self.temp_text = ''
            self.block_button_edit = ''
            self.block_button_num_edit = ''
            await Block(text='Текст изменен',
                  buttons=[('<- Назад', f'admin_{block_name}'), ('В админ меню', 'admin_menu')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
        elif 'admin_block_text' in call.data:
            block_name = call.data.replace('admin_block_text_', '')
            self.block_text_edit = block_name
            await Block(text='Введите новый текст в следующем сообщении:',
                  buttons=[('<- Назад', f'admin_{block_name}')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
        elif 'admin_block_buttons_num' in call.data:
            self.block_button_num_edit = call.data.replace('admin_block_buttons_num_', '')
            block_name = self.block_button_edit
            await Block(text='Введите новый текст для кнопки:',
                  buttons=[('<- Назад', f'admin_{block_name}')],
                  edit=True,
                  bd=self.bd,
                  anyway=True,
                  ).place_block(call)
        elif 'admin_block_buttons' in call.data:
            block_name = call.data.replace('admin_block_buttons_', '')
            self.block_button_edit = block_name
            await Block(text='Выберите кнопку:',
                  buttons=[*[(text, f'{'admin_block_buttons_num_'+str(i)}') for i, (text, call_data) in enumerate(Text.dop[block_name]['buttons'])], ('<- Назад', f'admin_{block_name}')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
        elif 'admin_block' in call.data:
            self.temp_text = ''
            self.block_text_edit = ''
            self.block_button_edit = ''
            self.block_button_num_edit = ''
            block_name = call.data.replace('admin_', '')
            await Block(text='\n\n'.join([f'Текст блока {block_name}', f'{Text.dop[block_name]["text"]}', f'Кнопки блока {block_name}', f'{'\n'.join([f'{button_text} -> {call_data}' for button_text, call_data in Text.dop[block_name]["buttons"]])}']),
                  buttons=[('Изменить текст', f'admin_block_text_{block_name}'), ('Изменить кнопку', f'admin_block_buttons_{block_name}'), ('<- Назад', 'admin_block')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)

    async def admin_timer(self, call):
        if call.data == 'admin_timer':
            self.admin_timer_change_time = False
            self.admin_timer_text_timerOver = False
            self.temp_text = ''
            self.admin_timer_restart = False
            self.admin_timer_close = False
            self.admin_timer_paymentStart = False
            await Block(text='Ти в разделе изменения таймера', 
                buttons=[('Поменять длительность таймера', 'admin_timer_change_time'), ('Рестарт таймера всем пользователям', 'admin_timer_restart'), ('Текст когда время закончится', 'admin_timer_text_timerOver'), ('Текст когда доступ к боту закроется', 'admin_timer_close'), ('Текст когда появилось окно оплаты', 'admin_timer_paymentStart'),('В админ меню', 'admin_menu')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_change_time':
            self.admin_timer_change_time = True
            await Block(text='Напиши время в часах(для теста минуты)', 
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_change_time_yes':
            time = self.temp_text
            self.temp_text = ''
            self.admin_timer_change_time = False
            Text.timer_settings['how_long'] = int(time)
            await self.update_dop_text_file()
            await Block(text='Таймер изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_restart':
            self.admin_timer_restart = True
            await Block(text='На сколько часов таймер перезапустить(для теста минуты)?',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_restart_time_yes':
            time = self.temp_text
            self.temp_text = ''
            self.admin_timer_restart = False
            for user in self.bd.get_all_users():
                if user[8] == 0:
                    await self.set_timer(user[1], int(time))
                    await self.bot.send_message(chat_id=user[1], text=Text.timer_settings['new_timer_text'])
            await Block(text='Таймер перезапущен',
                  buttons=[('<- Назад', 'admin_timer')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
        elif call.data == 'admin_timer_text_timerOver':
            self.admin_timer_text_timerOver = True
            await Block(text=f'Текущий текст\n\n{Text.timer_settings['timer_is_over_text']}\n\nЧтобы изменить текст напишите его в следующем сообщении',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_text_timerOver_yes':
            text = self.temp_text
            self.temp_text = ''
            self.admin_timer_text_timerOver = False
            Text.timer_settings['timer_is_over_text'] = text
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_close':
            self.admin_timer_close = True
            await Block(text=f'Текущий текст\n\n{Text.timer_settings['end_of_timer_text']}\n\nЧтобы изменить текст напишите его в следующем сообщении',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_close_yes':
            text = self.temp_text
            self.temp_text = ''
            self.admin_timer_close = False
            Text.timer_settings['end_of_timer_text'] = text
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_paymentStart':
            self.admin_timer_paymentStart = True
            await Block(text=f'Текущий текст\n\n{Text.timer_settings["new_timer_text"]}\n\nЧтобы изменить текст напишите его в следующем сообщении',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_paymentStart_yes':
            text = self.temp_text
            self.temp_text = ''
            self.admin_timer_paymentStart = False
            Text.timer_settings['new_timer_text'] = text
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        
    async def admin_send(self, call):
        if call.data == 'admin_send':
            await Block(text='Ти в разделе отправки сообщений', 
                buttons=[('Отправить сообщение', 'admin_send_message'), ('Отправить фото', 'admin_send_photo'), ('В админ меню', 'admin_menu')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_send_message':
            self.send_message = True
            await Block(text='Напиши текст сообщения', 
                buttons=[('<- Назад', 'admin_send')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_send_message_all':
            await self.send_message_helper(call, True, True)
        elif call.data == 'admin_send_message_noprime':
            await self.send_message_helper(call, False, True)
        elif call.data == 'admin_send_message_prime':
            await self.send_message_helper(call, True, False)
        elif call.data == 'admin_send_photo':
            self.send_photo = True
            await Block(text='Отправь фото', 
                buttons=[('<- Назад', 'admin_send')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_send_photo_all':
            await self.send_photo_helper(call, True, True)
        elif call.data == 'admin_send_photo_noprime':
            await self.send_photo_helper(call, False, True)
        elif call.data == 'admin_send_photo_prime':
            await self.send_photo_helper(call, True, False)
    
    async def send_photo_helper(self, call, prime=False, noprime=False):
        photo = self.temp_photo	
        self.temp_photo = None
        self.send_photo = False
        for user in self.bd.get_all_users():
            if prime and user[4]:
                await self.bot.send_photo(user[1], photo)
            if noprime and not user[4]:
                await self.bot.send_photo(user[1], photo)
        await Block(text='Фото отправлено', 
                buttons=[('В админ меню', 'admin_menu')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)

    async def send_message_helper(self, call, prime=False, noprime=False):
        text = self.temp_text
        self.temp_text = ''
        self.send_message = False
        for user in self.bd.get_all_users():
            if prime and user[4]:
                await self.bot.send_message(user[1], text)
            if noprime and not user[4]:
                await self.bot.send_message(user[1], text)
        await Block(text='Сообщения отправлены', 
                buttons=[('В админ меню', 'admin_menu')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)

    async def admin_menu(self, call):
        if call.data == 'admin_menu':
            await Block(text=Text.block_admin['text'],
                  buttons=Text.block_admin['buttons'],
                  anyway=True,
                  edit=True,
                  bd=self.bd
                  ).place_block(call)
    
    async def user(self, call):
        if 'menu' in call.data:
            await Block(text=Text.block_start['text'], 
                  buttons=Text.block_start['buttons'],
                  edit=Text.block_start['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'channel':
            await Block(text=Text.block_channel['text'], 
                  buttons=Text.block_channel['buttons'],
                  edit=Text.block_channel['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'choose_time':
            if self.bd.get_user(call.message.chat.id)[0][7] == None and self.bd.get_user(call.message.chat.id)[0][8] == 0:
                await self.set_timer(call.message.chat.id)
            await Block(text=Text.block_choose_time['text'], 
                  buttons=Text.block_choose_time['buttons'],
                  edit=Text.block_choose_time['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'question':
            await Block(text=Text.block_question['text'],
                  buttons=Text.block_question['buttons'],
                  edit=Text.block_question['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'myPrime':
            await Block(text=(Text.block_myPrime['text'] + f'\n\n{'https://t.me/+mtojuZOTFE4zMTIy'}' + f'\n\nДо: {self.bd.get_user(call.message.chat.id)[0][5]}') if self.bd.get_user(call.message.chat.id)[0][4] == True else 'У тебя пока нет подписок',
                  buttons=Text.block_myPrime['buttons'],
                  edit=Text.block_myPrime['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif 'time' in call.data:
            await Block(text=Text.block_choose_payment['text'], 
                  buttons=Text.block_choose_payment['buttons'],
                  edit=Text.block_choose_payment['edit'],
                  dop_callback='_'+call.data.split('_')[-1],
                  bd=self.bd
                  ).place_block(call)
        elif 'crypto' in call.data:
            CRYPTO = os.getenv('CRYPTO')
            if CRYPTO == 'True':
                await Block(text=Text.block_crypto['text']+'\n'+call.data.split('_')[-1], 
                    buttons=Text.block_crypto['buttons'],
                    edit=Text.block_crypto['edit'],
                    dop_callback='_'+call.data.split('_')[-1],
                    bd=self.bd
                    ).place_block(call)
            else:
                await Block(
                    text='Пока не доступно',
                    buttons=[('<- Назад', 'choose_time')],
                    edit=True,
                    bd=self.bd
                ).place_block(call)
        elif 'lavatopusd' in call.data:
            LAVATOP = os.getenv('LAVATOP')
            if LAVATOP == 'True':
                await Block(text=Text.block_lavatopusd['text'] + f'\n\n{[item for item in Text.buttons_list if item[1] == call.data.split('_')[-1]][0]}', 
                    buttons=Text.block_lavatopusd['buttons'],
                    edit=Text.block_lavatopusd['edit'],
                    dop_callback='_'+call.data.split('_')[-1],
                    bd=self.bd
                    ).place_block(call)
            else:
                await Block(
                    text='Пока не доступно',
                    buttons=[('<- Назад', 'choose_time')],
                    edit=True,
                    bd=self.bd
                ).place_block(call)
        elif 'for_free' in call.data:
            # ASYNC
            self.bd.set_have_prime(call.message.chat.id, True)
            self.bd.set_had_prime(call.message.chat.id, True)
            self.bd.set_end_of_prime(call.message.chat.id, (datetime.now() + timedelta(days=30*int(call.data.split('_')[-1]))).strftime("%Y-%m-%d"))
            await Block(text=Text.block_got_access['text'] + f'\n{self.link_on_chanel}', 
                  buttons=Text.block_got_access['buttons'],
                  edit=Text.block_got_access['edit'],
                  bd=self.bd
                  ).place_block(call)

    async def handle(self, call):
        if call.data.startswith('admin_menu'):
            await self.admin_menu(call)
        elif call.data.startswith('admin_timer'):
            await self.admin_timer(call)
        elif call.data.startswith('admin_block'):
            await self.admin_block(call)
        elif call.data.startswith('admin_send'):
            await self.admin_send(call)
        else:
            await self.user(call)

    

class MessageHandler:
    def __init__(self, bot, callback_handler: CallbackHandler):
        self.bot = bot
        self.callback_handler = callback_handler

    async def block_text_edit(self, message):
        self.callback_handler.temp_text = message.text
        await JustBlock(text=f'Поменять текст {self.callback_handler.block_text_edit}?',
              buttons=[('Да', 'admin_block_text_change'), ('Нет', 'admin_block')],
              ).place_block(message)
    
    async def block_button_edit(self, message):
        self.callback_handler.temp_text = message.text
        await JustBlock(text=f'Поменять кнопки {self.callback_handler.block_button_edit}?',
              buttons=[('Да', 'admin_block_button_change'), ('Нет', 'admin_block')],
              ).place_block(message)
    
    async def send_message(self, message):
        self.callback_handler.temp_text = message.text
        await JustBlock(text=f'Отправить сообщение:',
              buttons=[('Всем', 'admin_send_message_all'), ('Всем без подписки', 'admin_send_message_noprime'), ('Всем с подпиской', 'admin_send_message_prime'), ('Не отправлять', 'admin_send')],
              ).place_block(message)
    
    async def send_photo(self, message: types.Message):
        self.callback_handler.temp_photo = message.photo[-1].file_id
        await JustBlock(text=f'Отправить фото:',
              buttons=[('Всем', 'admin_send_photo_all'), ('Всем без подписки', 'admin_send_photo_noprime'), ('Всем с подпиской', 'admin_send_photo_prime'), ('Не отправлять', 'admin_send')],
              ).place_block(message)
    
    async def admin_timer_change_time(self, message):
        if message.text.isdigit():
            self.callback_handler.temp_text = message.text
            await JustBlock(text=f'Изменить время таймера?',
                  buttons=[('Да', 'admin_timer_change_time_yes'), ('Нет', 'admin_timer')],
                  ).place_block(message)
        else:
            await JustBlock(text='Нужно ввести число',
                  buttons=[('В меню таймера', 'admin_timer')],
                  ).place_block(message)
    
    async def admin_timer_restart(self, message):
        if message.text.isdigit():
            self.callback_handler.temp_text = message.text
            await JustBlock(text=f'Продолжить?',
                  buttons=[('Да', 'admin_timer_restart_time_yes'), ('Нет', 'admin_timer')],
                  ).place_block(message)
        else:
            await JustBlock(text='Нужно ввести число',
                  buttons=[('В меню таймера', 'admin_timer')],
                  ).place_block(message)
        
    async def admin_timer_text_timerOver(self, message):
        self.callback_handler.temp_text = message.text
        await JustBlock(text=f'Применить?',
              buttons=[('Да', 'admin_timer_text_timerOver_yes'), ('Нет', 'admin_timer')],
              ).place_block(message)
    
    async def admin_timer_close(self, message):
        self.callback_handler.temp_text = message.text
        await JustBlock(text=f'Применить?',
              buttons=[('Да', 'admin_timer_close_yes'), ('Нет', 'admin_timer')],
              ).place_block(message)
    
    async def admin_timer_paymentStart(self, message):
        self.callback_handler.temp_text = message.text
        await JustBlock(text=f'Применить?',
              buttons=[('Да', 'admin_timer_paymentStart_yes'), ('Нет', 'admin_timer')],
              ).place_block(message)

    async def handle(self, message):
        if self.callback_handler.block_text_edit != '':
            await self.block_text_edit(message)
        elif self.callback_handler.block_button_edit != '' and self.callback_handler.block_button_num_edit != '':
            await self.block_button_edit(message)
        elif self.callback_handler.send_message == True:
            await self.send_message(message)
        elif self.callback_handler.send_photo == True:
            await self.send_photo(message)
        elif self.callback_handler.admin_timer_change_time == True:
            await self.admin_timer_change_time(message)
        elif self.callback_handler.admin_timer_restart == True:
            await self.admin_timer_restart(message)
        elif self.callback_handler.admin_timer_text_timerOver == True:
            await self.admin_timer_text_timerOver(message)
        elif self.callback_handler.admin_timer_close == True:
            await self.admin_timer_close(message)
        elif self.callback_handler.admin_timer_paymentStart == True:
            await self.admin_timer_paymentStart(message)



class JustBlock:
    def __init__(self, text, buttons):
        self.text = text
        self.buttons = buttons
    
    async def place_block(self, message):
        buttons = [[InlineKeyboardButton(text=button_text, callback_data=call_data)] for button_text, call_data in self.buttons]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(text=self.text, reply_markup=markup)


class Block:
    def __init__(self, text:str, buttons:list[tuple], bd, edit:bool=False, dop_callback:str="", anyway:bool=False):
        self.text = text
        self.buttons = buttons
        self.edit = edit
        self.dop_callback = dop_callback
        self.anyway = anyway
        self.bd = bd
    
    async def place_block(self, call: types.CallbackQuery):
        if (timer := self.bd.get_user(call.message.chat.id)[0][7]) == None or datetime.strptime(timer, "%Y-%m-%d %H:%M:%S.%f") > datetime.now() or self.anyway or self.bd.get_user(call.message.chat.id)[0][8] == 1:
            buttons = [[InlineKeyboardButton(text=button_text, callback_data=call+self.dop_callback)] for button_text, call in self.buttons]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            if self.edit:
                await call.message.edit_text(text=self.text, inline_message_id=call.inline_message_id, reply_markup=markup)
            else:
                await call.message.answer(text=self.text, reply_markup=markup)
        else:
            if self.edit:
                await call.message.edit_text(text=Text.timer_settings['timer_is_over_text'], inline_message_id=call.inline_message_id)
            else:
                await call.message.answer(text=Text.timer_settings['timer_is_over_text'])