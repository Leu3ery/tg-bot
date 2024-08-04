timer_settings = {'how_long': 1, 'timer_is_over_text':'''Твое время вышло. Включи уведомления чтоби успеть в следующий раз...''', 'new_timer_text':'''Появилось окно оплати. Жми /start''', 'end_of_timer_text':'''Доступ к боту закроется в'''}
block_noprime = {'buttons': [('Да', 'choose_time'), ('Нет', 'menu')], 'text': '''Tи потерял доступ к каналу. Хочешь получить снова?'''}

block_start = {'edit':True, 'buttons':[('Подробносри канала', 'channel'), ('Оплата', 'choose_time'), ('Задать вопрос', 'question')], 'text':'''Приветствую 👋
Этот бот поможет тебе попасть в приватное сообщество Магомеда Абакарова 🚀
Подписка ежемесячная, оплату принимаем в любой валюте.'''}
block_channel = {'edit':True, 'buttons':[('В меню', 'menu')], 'text':'''В Академии Магомеда Абакарова👇
                 
✅ Все инструменты восстановления своего здоровья, собранные в единую систему, которую ты сможешь внедрить в свою жизнь уже сегодня.
                 
✅ Статьи, гайды по восстановлению всех систем организма, треды, эфиры с ответами на вопросы и тайм кодами, которые постоянно обновляются.
                 
✅ Сообщество сильных и свободных людей, которые ежедневно развиваются во всех ветвях жизни.
                 
✅ Все мои проекты, которые раньше продавались по отдельности за высокую цену: курс по заработку на нейросетях, курс по развитию мозга и памяти, курс по игре на гитаре.

Никаких доплат, тарифов и прочих заморочек. Все и сразу в одном месте.
И помни, что вчера ты говорил «завтра»
Увидимся в Академии.'''}
block_question = {'edit':True, 'buttons':[('В меню', 'menu')], 'text':'''Свяжитесь с нами, если у вас есть вопросы или проблемы
Ссылка на мой аккаунт ниже:👇'''}
block_choose_time = {'edit':True, 'buttons':[('1 Месяц', 'time_1'), ('3 Месяца', 'time_3'), ('НАВСЕГДА', 'time_forever'), ('В меню', 'menu')], 'text':'''Выберите тариф из списка ниже: 👇'''}
block_choose_payment = {'edit':True, 'buttons':[('Крипта', 'crypto'), ('Банковская карта(Долар)', 'lavatopusd'), ('В меню', 'menu')], 'text':'''Выберите способ оплаты 👇'''}
block_crypto = {'edit':True, 'buttons':[('Получить безплатно', 'for_free'), ('В меню', 'menu')], 'text':'''Оплата по крипте пока не доступна'''}
block_lavatopusd = {'edit':True, 'buttons':[('Получить безплатно', 'for_free'), ('В меню', 'menu')], 'text':'''Оплата по банковской карте пока не доступна'''}
block_got_access = {'edit':True, 'buttons':[('В меню', 'menu')], 'text':'''Ты получил доступ к каналу: 
https://t.me/+mtojuZOTFE4zMTIy'''}


block_admin = {'buttons':[('Внешний вид', 'admin_block'), ('Таймер', 'admin_timer'), ('Общая розсылка', 'admin_send')], 'text':'''Ти в админ меню. Виберите действие: 👇'''}


dop = {
    'block_start':block_start,
    'block_channel':block_channel,
    'block_question':block_question,
    'block_choose_time':block_choose_time,
    'block_choose_payment':block_choose_payment,
    'block_crypto':block_crypto,
    'block_lavatopusd':block_lavatopusd,
    'block_got_access':block_got_access,
    'block_noprime':block_noprime,
}