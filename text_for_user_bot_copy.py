timer_settings = {'how_long': 3, 'timer_is_over_text': 'Твое время вышло. Включи уведомления чтоби успеть в следующий раз...', 'new_timer_text': 'Появилось окно оплати. Жми /start', 'end_of_timer_text': 'Доступ к боту закроется в'}
block_noprime = {'buttons': [('Да', 'choose_time'), ('Нет', 'menu')], 'text': 'Tи потерял доступ к каналу. Хочешь получить снова?'}
block_start = {'edit': True, 'buttons': [('Про канал', 'channel'), ('Оплата', 'choose_time'), ('Задать вопрос', 'question'), ('Мои подписки', 'myPrime')], 'text': 'Приветствую 👋\nЭтот бот поможет тебе попасть в приватное сообщество Магомеда Абакарова 🚀\nПодписка ежемесячная, оплату принимаем в любой валюте.'}
block_channel = {'edit': True, 'buttons': [('В меню', 'menu')], 'text': 'В Академии Магомеда Абакарова👇\n                 \n✅ Все инструменты восстановления своего здоровья, собранные в единую систему, которую ты сможешь внедрить в свою жизнь уже сегодня.\n                 \n✅ Статьи, гайды по восстановлению всех систем организма, треды, эфиры с ответами на вопросы и тайм кодами, которые постоянно обновляются.\n                 \n✅ Сообщество сильных и свободных людей, которые ежедневно развиваются во всех ветвях жизни.\n                 \n✅ Все мои проекты, которые раньше продавались по отдельности за высокую цену: курс по заработку на нейросетях, курс по развитию мозга и памяти, курс по игре на гитаре.\n\nНикаких доплат, тарифов и прочих заморочек. Все и сразу в одном месте.\nИ помни, что вчера ты говорил «завтра»\nУвидимся в Академии.'}
block_question = {'edit': True, 'buttons': [('В меню', 'menu')], 'text': 'Свяжитесь с нами, если у вас есть вопросы или проблемы\nСсылка на мой аккаунт ниже:👇'}
block_choose_time = {'edit': True, 'buttons': [('1 Месяц', 'time_1'), ('6 Месяцев', 'time_6'), ('12 Месяцев', 'time_12'), ('В меню', 'menu')], 'text': 'Выберите тариф из списка ниже: 👇'}
block_choose_payment = {'edit': True, 'buttons': [('Крипта', 'crypto'), ('Банковская карта(Долар)', 'lavatopusd'), ('В меню', 'menu')], 'text': 'Выберите способ оплаты 👇'}
block_crypto = {'edit': True, 'buttons': [('Получить безплатно', 'for_free'), ('В меню', 'menu')], 'text': 'Оплата по крипте пока не доступна'}
block_lavatopusd = {'edit': True, 'buttons': [('Получить безплатно', 'for_free'), ('В меню', 'menu')], 'text': 'Оплата по банковской карте пока не доступна'}
block_got_access = {'edit': True, 'buttons': [('В меню', 'menu')], 'text': 'Ты получил доступ к каналу: '}
block_admin = {'buttons': [('Внешний вид', 'admin_block'), ('Таймер', 'admin_timer'), ('Общая розсылка', 'admin_send')], 'text': 'Ти в админ меню. Виберите действие: 👇'}
block_myPrime = {'edit': True, 'buttons': [('В меню', 'menu')], 'text': 'У тебя есть доступ к каналу:'}

dop = {
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
}
    