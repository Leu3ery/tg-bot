import text_for_user_bot_copy as Text
import lavatop_api as Lava
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    email = State()
    currency = State()
    time = State()

    block_name = State()
    block_text = State()
    block_button_num = State()
    block_button_text = State()

    timer_change_time = State()
    timer_restart_time = State()
    timer_text_timerOver = State()
    timer_close = State()
    timer_paymentStart = State()

    send_message = State()
    send_photo = State()


class UserBot:
    def __init__(self, token: str, bd, link_on_chanel:str, lavatop_api):
        USER_BOT = os.getenv('USER_BOT')
        if USER_BOT == 'True':
            self.bd = bd
            self.bot = Bot(token=token)
            self.dp = Dispatcher()
            self.link_on_chanel = link_on_chanel
            self.lavatop_api = lavatop_api
            self.callback_handler = CallbackHandler(self.bot, self.bd, self.set_timer, self.update_dop_text_file, self.link_on_chanel, self.lavatop_api)
            self.message_handler = MessageHandler(self.bot, self.callback_handler)
            self.setup_handlers()
        else:
            print('USER_BOT = False')

    def setup_handlers(self):
        @self.dp.message(CommandStart())
        async def on_start(message: types.Message, state: FSMContext):
            await state.clear()
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
        async def admin(message: types.Message, state: FSMContext):
            # ASSENTYAL if message.chat.id == MODERATOR
            await state.clear()
            self.bd.add_new_user(message.chat.id)
            self.bd.set_start_of_using_bot(message.chat.id, datetime.now().strftime("%Y-%m-%d"))
            self.bd.set_nickname(message.chat.id, message.chat.username)
            buttons = [[InlineKeyboardButton(text=button_text, callback_data=call)] for button_text, call in Text.block_admin['buttons']]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer(Text.block_admin['text'], reply_markup=markup)
        
        @self.dp.message(Command('noprime'))
        async def on_noprime(message: types.Message):
            self.bd.set_have_prime(message.chat.id, False)
            self.bd.set_end_of_prime(message.chat.id, None)

        @self.dp.message(Command('notimer'))
        async def on_notimer(message: types.Message):
            self.bd.set_end_of_timer(message.chat.id, None)
            await self.bot.send_message(chat_id=message.chat.id, text=Text.timer_settings['new_timer_text'])
        
        @self.dp.callback_query(lambda c: c.data)
        async def process_callback(call: types.CallbackQuery, state: FSMContext):
            await self.callback_handler.handle(call, state)
        
        @self.dp.message()
        async def on_message(message: types.Message, state: FSMContext):
            await self.message_handler.handle(message, state)
             
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
block_lavatop = {Text.block_lavatop}
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
    'block_lavatop': block_lavatop,
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
    def __init__(self, bot, bd, set_timer, update_dop_text_file, link_on_chanel, lavatop_api):
        self.bot = bot
        self.bd = bd
        self.set_timer = set_timer
        self.update_dop_text_file = update_dop_text_file
        self.link_on_chanel = link_on_chanel
        self.lavatop_api = lavatop_api
    

    async def admin_block(self, call, state: FSMContext):
        if call.data == 'admin_block':
            await state.clear()
            await Block(text="Ти в разделе изменения блоков", 
            buttons=[('Стартовый блок', 'admin_block_start'), ('Канал', 'admin_block_channel'), ('Вопросы', 'admin_block_question'), ('Подписки', 'admin_block_myPrime'), ('Выбор времени', 'admin_block_choose_time'), ('Выбор способа оплаты', 'admin_block_choose_payment'), ('Криптовалюта', 'admin_block_crypto'), ('Лаватоп', 'admin_block_lavatop'), ('При получении доступа', 'admin_block_got_access'), ('При окончании премиума', 'admin_block_noprime'), ('В админ меню', 'admin_menu')],
            edit=True,
            bd=self.bd,
            anyway=True
            ).place_block(call)
        elif call.data == 'admin_block_text_change':
            data = await state.get_data()
            block_name = data['block_name']
            text = data['block_text']
            Text.dop[block_name]['text'] = text
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                  buttons=[('<- Назад', f'admin_{block_name}'), ('В админ меню', 'admin_menu')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
            await state.clear()
        elif call.data == 'admin_block_button_change':
            data = await state.get_data()
            block_name = data['block_name']
            block_button_num = data['block_button_num']
            block_button_text = data['block_button_text']
            Text.dop[block_name]['buttons'][int(block_button_num)] = (block_button_text, Text.dop[block_name]['buttons'][int(block_button_num)][1])
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                  buttons=[('<- Назад', f'admin_{block_name}'), ('В админ меню', 'admin_menu')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
            await state.clear()
        elif 'admin_block_text' in call.data:
            block_name = call.data.replace('admin_block_text_', '')
            await state.update_data(block_name=block_name)
            await state.set_state(Form.block_text)
            await Block(text='Введите новый текст в следующем сообщении:',
                  buttons=[('<- Назад', f'admin_{block_name}')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
        elif 'admin_block_buttons_num' in call.data:
            button_num = call.data.replace('admin_block_buttons_num_', '')
            await state.update_data(block_button_num=button_num)
            await state.set_state(Form.block_button_text)
            data = await state.get_data()
            block_name = data['block_name']
            await Block(text='Введите новый текст для кнопки:',
                  buttons=[('<- Назад', f'admin_{block_name}')],
                  edit=True,
                  bd=self.bd,
                  anyway=True,
                  ).place_block(call)
        elif 'admin_block_buttons' in call.data:
            block_name = call.data.replace('admin_block_buttons_', '')
            await state.update_data(block_name=block_name)
            await Block(text='Выберите кнопку:',
                  buttons=[*[(text, f'{'admin_block_buttons_num_'+str(i)}') for i, (text, call_data) in enumerate(Text.dop[block_name]['buttons'])], ('<- Назад', f'admin_{block_name}')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
        elif 'admin_block' in call.data:
            await state.clear()
            block_name = call.data.replace('admin_', '')
            await Block(text='\n\n'.join([f'Текст блока {block_name}', f'{Text.dop[block_name]["text"]}', f'Кнопки блока {block_name}', f'{'\n'.join([f'{button_text} -> {call_data}' for button_text, call_data in Text.dop[block_name]["buttons"]])}']),
                  buttons=[('Изменить текст', f'admin_block_text_{block_name}'), ('Изменить кнопку', f'admin_block_buttons_{block_name}'), ('<- Назад', 'admin_block')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)

    async def admin_timer(self, call, state: FSMContext):
        if call.data == 'admin_timer':
            await state.clear()
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
            await state.set_state(Form.timer_change_time)
            await Block(text='Напиши время в часах(для теста минуты)', 
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_change_time_yes':
            data = await state.get_data()
            time = data['timer_change_time']
            await state.clear()
            Text.timer_settings['how_long'] = int(time)
            await self.update_dop_text_file()
            await Block(text='Таймер изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_restart':
            await state.set_state(Form.timer_restart_time)
            await Block(text='На сколько часов таймер перезапустить(для теста минуты)?',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_restart_time_yes':
            data = await state.get_data()
            time = data['timer_restart_time']
            await state.clear()
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
            await state.set_state(Form.timer_text_timerOver)
            await Block(text=f'Текущий текст\n\n{Text.timer_settings['timer_is_over_text']}\n\nЧтобы изменить текст напишите его в следующем сообщении',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_text_timerOver_yes':
            data = await state.get_data()
            text = data['timer_text_timerOver']
            await state.clear()
            Text.timer_settings['timer_is_over_text'] = text
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_close':
            await state.set_state(Form.timer_close)
            await Block(text=f'Текущий текст\n\n{Text.timer_settings['end_of_timer_text']}\n\nЧтобы изменить текст напишите его в следующем сообщении',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_close_yes':
            data = await state.get_data()
            text = data['timer_close']
            await state.clear()
            Text.timer_settings['end_of_timer_text'] = text
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_paymentStart':
            await state.set_state(Form.timer_paymentStart)
            await Block(text=f'Текущий текст\n\n{Text.timer_settings["new_timer_text"]}\n\nЧтобы изменить текст напишите его в следующем сообщении',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_timer_paymentStart_yes':
            data = await state.get_data()
            text = data['timer_paymentStart']
            await state.clear()
            Text.timer_settings['new_timer_text'] = text
            await self.update_dop_text_file()
            await Block(text='Текст изменен',
                buttons=[('<- Назад', 'admin_timer')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        
    async def admin_send(self, call, state: FSMContext):
        if call.data == 'admin_send':
            await state.clear()
            await Block(text='Ти в разделе отправки сообщений', 
                buttons=[('Отправить сообщение', 'admin_send_message'), ('Отправить фото', 'admin_send_photo'), ('В админ меню', 'admin_menu')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_send_message':
            await state.set_state(Form.send_message)
            await Block(text='Напиши текст сообщения', 
                buttons=[('<- Назад', 'admin_send')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_send_message_all':
            await self.send_message_helper(call, state, True, True)
        elif call.data == 'admin_send_message_noprime':
            await self.send_message_helper(call, state, False, True)
        elif call.data == 'admin_send_message_prime':
            await self.send_message_helper(call, state, True, False)
        elif call.data == 'admin_send_photo':
            await state.set_state(Form.send_photo)
            await Block(text='Отправь фото', 
                buttons=[('<- Назад', 'admin_send')],
                edit=True,
                bd=self.bd,
                anyway=True
                ).place_block(call)
        elif call.data == 'admin_send_photo_all':
            await self.send_photo_helper(call, state, True, True)
        elif call.data == 'admin_send_photo_noprime':
            await self.send_photo_helper(call, state, False, True)
        elif call.data == 'admin_send_photo_prime':
            await self.send_photo_helper(call, state, True, False)
    
    async def send_photo_helper(self, call, state: FSMContext, prime=False, noprime=False):
        data = await state.get_data()
        photo = data['send_photo']
        await state.clear()
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

    async def send_message_helper(self, call, state: FSMContext, prime=False, noprime=False):
        data = await state.get_data()
        text = data['send_message']
        await state.clear()
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

    async def admin_menu(self, call: types.CallbackQuery, state: FSMContext):
        await state.clear()
        if call.data == 'admin_menu':
            await Block(text=Text.block_admin['text'],
                  buttons=Text.block_admin['buttons'],
                  anyway=True,
                  edit=True,
                  bd=self.bd
                  ).place_block(call)
    
    async def user(self, call: types.CallbackQuery, state: FSMContext):
        if 'menu' in call.data:
            await state.clear()
            await Block(text=Text.block_start['text'], 
                  buttons=Text.block_start['buttons'],
                  edit=Text.block_start['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'channel':
            await state.clear()
            await Block(text=Text.block_channel['text'], 
                  buttons=Text.block_channel['buttons'],
                  edit=Text.block_channel['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'choose_time':
            await state.clear()
            if self.bd.get_user(call.message.chat.id)[0][7] == None and self.bd.get_user(call.message.chat.id)[0][8] == 0:
                await self.set_timer(call.message.chat.id)
            await Block(text=Text.block_choose_time['text'], 
                  buttons=Text.block_choose_time['buttons'],
                  edit=Text.block_choose_time['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'question':
            await state.clear()
            await Block(text=Text.block_question['text'],
                  buttons=Text.block_question['buttons'],
                  edit=Text.block_question['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif call.data == 'myPrime':
            await state.clear()
            await Block(text=(Text.block_myPrime['text'] + f'\n\n{'https://t.me/+mtojuZOTFE4zMTIy'}' + f'\n\nДо: {self.bd.get_user(call.message.chat.id)[0][5]}') if self.bd.get_user(call.message.chat.id)[0][4] == True else 'У тебя пока нет подписок',
                  buttons=Text.block_myPrime['buttons'],
                  edit=Text.block_myPrime['edit'],
                  bd=self.bd
                  ).place_block(call)
        elif 'time' in call.data:
            await state.clear()
            await Block(text=Text.block_choose_payment['text'], 
                  buttons=Text.block_choose_payment['buttons'],
                  edit=Text.block_choose_payment['edit'],
                  dop_callback='_'+call.data.split('_')[-1],
                  bd=self.bd
                  ).place_block(call)
        elif 'crypto' in call.data:
            await state.clear()
            CRYPTO = os.getenv('CRYPTO')
            if CRYPTO == 'True':
                await Block(text=Text.block_crypto['text']+'\n'+call.data.split('_')[-1], 
                    buttons=Text.block_crypto['buttons'],
                    edit=Text.block_crypto['edit'],
                    dop_callback='_'+call.data.split('_')[-1],
                    bd=self.bd,
                    anyway=True
                    ).place_block(call)
            else:
                await Block(
                    text='Пока не доступно',
                    buttons=[('<- Назад', 'choose_time')],
                    edit=True,
                    bd=self.bd,
                    anyway=True
                ).place_block(call)
        elif 'lavatop' in call.data:
            await state.clear()
            LAVATOP = os.getenv('LAVATOP')
            if LAVATOP == 'True':
                await Block(text=Text.block_lavatop['text'], 
                    buttons=Text.block_lavatop['buttons'],
                    edit=Text.block_lavatop['edit'],
                    dop_callback='_'+call.data.split('_')[-1],
                    bd=self.bd,
                    anyway=True
                    ).place_block(call)
            else:
                await Block(
                    text='Пока не доступно',
                    buttons=[('<- Назад', 'choose_time')],
                    edit=True,
                    bd=self.bd,
                    anyway=True
                ).place_block(call)
        elif 'currency' in call.data:
            currency = call.data.split('_')[-2]
            time = call.data.split('_')[-1]
            await Block(text='Введи почту для оплаты в следующем формате: example@gmail.com',
                  buttons=[('<- Назад', 'choose_time')],
                  edit=True,
                  bd=self.bd,
                  anyway=True
                  ).place_block(call)
            await state.update_data(currency=currency)
            await state.update_data(time=time)
            await state.set_state(Form.email)
        elif 'final_payment' in call.data:
            data = await state.get_data()
            email = data['email']
            time = data['time']
            currency = data['currency']
            await state.clear()
            self.bd.set_email(call.message.chat.id, email)
            item = [i for i in Text.buttons_list if i[1] == time][0]
            response = self.lavatop_api.create_link(item[3] , currency, email)
            if response:
                response = response.json()
                url = response['paymentUrl']
                payment_id = response['id']
                buttons = [[InlineKeyboardButton(text='Оплатить', url=url)], [InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_payment_{time}_{payment_id}')]]
                markup = InlineKeyboardMarkup(inline_keyboard=buttons)
                await call.message.edit_text(text=f'Покупка подписки на {item[0]}', inline_message_id=call.inline_message_id, reply_markup=markup)
            else:
                await call.message.edit_text(text=f'Произошла ошибка (возможно вы ввели почту некорректно)', inline_message_id=call.inline_message_id)
        elif 'check_payment' in call.data:
            time = call.data.split('_')[-2]
            payment_id = call.data.split('_')[-1]
            response = self.lavatop_api.get_paymant_by_id(payment_id)
            if response:
                response = response.json()
                await self.bot.send_message(chat_id=call.message.chat.id, text=f'{response}')
                print(response)
                if response['status'] == 'completed':
                    print('Успешно оплачено')
                    await self.bot.send_message(chat_id=call.message.chat.id, text=f'Оплата завершена', reply_markup=None)
                    self.bd.set_have_prime(call.message.chat.id, True)
                    self.bd.set_had_prime(call.message.chat.id, True)
                    self.bd.set_end_of_prime(call.message.chat.id, (datetime.now() + timedelta(days=30*int(time))).strftime("%Y-%m-%d"))
                    await Block(text=Text.block_got_access['text'] + f'\n{self.link_on_chanel}', 
                        buttons=Text.block_got_access['buttons'],
                        edit=Text.block_got_access['edit'],
                        bd=self.bd,
                        anyway=True
                        ).place_block(call)
                else:
                    await self.bot.send_message(chat_id=call.message.chat.id, text=f'Оплата в процессе', reply_markup=None)
            else:
                await self.bot.send_message(chat_id=call.message.chat.id, text=f'Произошла ошибка', reply_markup=None)

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

    async def handle(self, call: types.CallbackQuery, state: FSMContext):
        if call.data.startswith('admin_menu'):
            await self.admin_menu(call, state)
        elif call.data.startswith('admin_timer'):
            await self.admin_timer(call, state)
        elif call.data.startswith('admin_block'):
            await self.admin_block(call, state)
        elif call.data.startswith('admin_send'):
            await self.admin_send(call, state)
        else:
            await self.user(call, state)
 

class MessageHandler:
    def __init__(self, bot, callback_handler: CallbackHandler):
        self.bot = bot
        self.callback_handler = callback_handler
    
    async def save_email(self, message: types.Message, state: FSMContext):
        if '@' in message.text and '.' in message.text and '.' in message.text[message.text.index('@'):]:
            await state.update_data(email=message.text)
            buttons = [[InlineKeyboardButton(text=button_text, callback_data=call)] for button_text, call in [('Да', 'final_payment'), ('<- Назад', 'choose_time')]]
            markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer('Подтвердить?', reply_markup=markup)
        else:
            await message.answer('Email введен некорректно')

    async def block_text_edit(self, message, state: FSMContext):
        # self.callback_handler.temp_text = message.text
        await state.update_data(block_text=message.text)
        data = await state.get_data()
        await JustBlock(text=f'Поменять текст {data['block_name']}?',
              buttons=[('Да', 'admin_block_text_change'), ('Нет', 'admin_block')],
              ).place_block(message)
    
    async def block_button_edit(self, message, state: FSMContext):
        await state.update_data(block_button_text=message.text)
        data = await state.get_data()
        # self.callback_handler.temp_text = message.text
        await JustBlock(text=f'Поменять кнопку {data['block_name']}?',
              buttons=[('Да', 'admin_block_button_change'), ('Нет', 'admin_block')],
              ).place_block(message)
    
    async def send_message(self, message, state: FSMContext):
        await state.update_data(send_message=message.text)
        await JustBlock(text=f'Отправить сообщение:',
              buttons=[('Всем', 'admin_send_message_all'), ('Всем без подписки', 'admin_send_message_noprime'), ('Всем с подпиской', 'admin_send_message_prime'), ('Не отправлять', 'admin_send')],
              ).place_block(message)
    
    async def send_photo(self, message: types.Message, state: FSMContext):
        await state.update_data(send_photo=message.photo[-1].file_id)
        await JustBlock(text=f'Отправить фото:',
              buttons=[('Всем', 'admin_send_photo_all'), ('Всем без подписки', 'admin_send_photo_noprime'), ('Всем с подпиской', 'admin_send_photo_prime'), ('Не отправлять', 'admin_send')],
              ).place_block(message)
    
    async def admin_timer_change_time(self, message, state: FSMContext):
        if message.text.isdigit():
            await state.update_data(timer_change_time=message.text)
            await JustBlock(text=f'Изменить время таймера?',
                  buttons=[('Да', 'admin_timer_change_time_yes'), ('Нет', 'admin_timer')],
                  ).place_block(message)
        else:
            await JustBlock(text='Нужно ввести число',
                  buttons=[('В меню таймера', 'admin_timer')],
                  ).place_block(message)
    
    async def admin_timer_restart(self, message, state: FSMContext):
        if message.text.isdigit():
            await state.update_data(timer_restart_time=message.text)
            await JustBlock(text=f'Продолжить?',
                  buttons=[('Да', 'admin_timer_restart_time_yes'), ('Нет', 'admin_timer')],
                  ).place_block(message)
        else:
            await JustBlock(text='Нужно ввести число',
                  buttons=[('В меню таймера', 'admin_timer')],
                  ).place_block(message)
        
    async def admin_timer_text_timerOver(self, message, state: FSMContext):
        await state.update_data(timer_text_timerOver=message.text)
        await JustBlock(text=f'Применить?',
              buttons=[('Да', 'admin_timer_text_timerOver_yes'), ('Нет', 'admin_timer')],
              ).place_block(message)
    
    async def admin_timer_close(self, message, state: FSMContext):
        await state.update_data(timer_close=message.text)
        await JustBlock(text=f'Применить?',
              buttons=[('Да', 'admin_timer_close_yes'), ('Нет', 'admin_timer')],
              ).place_block(message)
    
    async def admin_timer_paymentStart(self, message, state: FSMContext):
        await state.update_data(timer_paymentStart=message.text)
        await JustBlock(text=f'Применить?',
              buttons=[('Да', 'admin_timer_paymentStart_yes'), ('Нет', 'admin_timer')],
              ).place_block(message)
    


    async def handle(self, message: types.Message, state: FSMContext):
        # ASSENTYAL if message.chat.id == MODERATOR
        current_state = await state.get_state()
        if current_state == 'Form:email':
            await self.save_email(message, state)
        elif current_state == 'Form:block_text':
            await self.block_text_edit(message, state)
        elif current_state == 'Form:block_button_text':
            await self.block_button_edit(message, state)
        elif current_state == 'Form:timer_change_time':
            await self.admin_timer_change_time(message, state)
        elif current_state == 'Form:timer_restart_time':
            await self.admin_timer_restart(message, state)
        elif current_state == 'Form:timer_text_timerOver':
            await self.admin_timer_text_timerOver(message, state)
        elif current_state == 'Form:timer_close':
            await self.admin_timer_close(message, state)
        elif current_state == 'Form:timer_paymentStart':
            await self.admin_timer_paymentStart(message, state)
        elif current_state == 'Form:send_message':
            await self.send_message(message, state)
        elif current_state == 'Form:send_photo':
            await self.send_photo(message, state)


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