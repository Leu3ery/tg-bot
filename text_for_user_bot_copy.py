timer_settings = {'how_long': 60, 'timer_is_over_text': 'Твое время вышло. Включи уведомления чтобы успеть в следующий раз...', 'new_timer_text': 'Появилось окно оплати. Жми /start', 'end_of_timer_text': 'Доступ к боту закроется в'}
block_noprime = {'buttons': [('Да', 'choose_time'), ('Нет', 'menu')], 'text': 'Tи потерял доступ к каналу. Хочешь получить снова?'}
block_start = {'edit': True, 'buttons': [('Про канал', 'channel'), ('Оплата', 'choose_time'), ('Задать вопрос', 'question'), ('Мои подписки', 'myPrime')], 'text': '🩷'}
block_channel = {'edit': True, 'buttons': [('В меню', 'menu')], 'text': 'В Академии Магомеда Абакарова👇\n                 \n✅ Все инструменты восстановления своего здоровья, собранные в единую систему, которую ты сможешь внедрить в свою жизнь уже сегодня.\n                 \n✅ Статьи, гайды по восстановлению всех систем организма, треды, эфиры с ответами на вопросы и тайм кодами, которые постоянно обновляются.\n                 \n✅ Сообщество сильных и свободных людей, которые ежедневно развиваются во всех ветвях жизни.\n                 \n✅ Все мои проекты, которые раньше продавались по отдельности за высокую цену: курс по заработку на нейросетях, курс по развитию мозга и памяти, курс по игре на гитаре.\n\nНикаких доплат, тарифов и прочих заморочек. Все и сразу в одном месте.\nИ помни, что вчера ты говорил «завтра»\nУвидимся в Академии.'}
block_question = {'edit': True, 'buttons': [('В меню', 'menu')], 'text': 'Свяжитесь с нами, если у вас есть вопросы или проблемы\nСсылка на мой аккаунт ниже:👇'}
block_choose_time = {'edit': True, 'buttons': [('1 Месяц', 'time_1'), ('6 Месяцов', 'time_6'), ('12 Месяцев', 'time_12'), ('В меню', 'menu')], 'text': 'Выберите тариф из списка ниже: 👇'}
block_choose_payment = {'edit': True, 'buttons': [('Крипта', 'crypto'), ('Банковская карта', 'lavatopusd'), ('В меню', 'menu')], 'text': 'Выберите способ оплаты 👇'}
block_crypto = {'edit': True, 'buttons': [('Я отправил - ввести айди транзакции', 'id_input'), ('В меню', 'menu')], 'text': 'Тебе необходимо отправить'}
block_lavatop = {'edit': True, 'buttons': [('Рубль', 'currency_RUB'), ('Доллар', 'currency_USD'), ('Евро', 'currency_EUR'), ('В меню', 'menu')], 'text': 'Выберите валюту: 👇'}
block_got_access = {'edit': False, 'buttons': [('Мои подписки', 'myPrime'), ('В меню', 'menu')], 'text': 'Ты получил доступ к каналу: '}
block_admin = {'buttons': [('Внешний вид', 'admin_block'), ('Таймер', 'admin_timer'), ('Общая розсылка', 'admin_send')], 'text': 'Ти в админ меню. Виберите действие: 👇'}
block_myPrime = {'edit': True, 'buttons': [('В меню', 'menu')], 'text': 'У тебя есть доступ к каналу:'}

buttons_list = [('1 Месяц', '1', '1', '4ccc40c5-dabd-44aa-b4fb-27ae1cdfb987'), ('6 Месяцов', '6', '100', 'd4fee54e-d08b-41fd-a9fa-3262baa9763a'), ('12 Месяцев', '12', '160', '3e59480b-fae8-4cb3-b193-4ce89419c22b')]

dop = {
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
}
    