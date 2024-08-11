import text_for_user_bot_copy as Text
import lavatop_api as Lava

TRACKING_BOT_TOKEN = '5439229031:AAGqHP3y4Fu_Gdd0gVRc7NgAu-afBXc_6tI'
GROUP_ID = '-1002217130582'
# user_bot True/False
USER_BOT = 'True'
USER_BOT_TOKEN = '1792974481:AAE_fmb0cpUVJTf6dOGJrRYpuIe5tZ6EuEw'
CHANEL_LINK = 'https://t.me/+mtojuZOTFE4zMTIy'
buttons_list = [('1 Месяц', '1', '1', '4ccc40c5-dabd-44aa-b4fb-27ae1cdfb987'), ('6 Месяцов', '6', '100', 'd4fee54e-d08b-41fd-a9fa-3262baa9763a'), ('12 Месяцев', '12', '160', '3e59480b-fae8-4cb3-b193-4ce89419c22b')]
# lavatop True/False
LAVATOP = 'True'
LAVATOP_API = '5qrdAsdvjyj9yvXCWj7uEhQBP9rpEqkM2JXPVaVEWijM0Fgmt7CXKmG6NVDCMAzy'
# setup offer_id
# crypto True/False
CRYPTO = 'True'
CRYPTO_TOKEN = 'TUpjgCrB1np6vE93dPMRKNcCc35TstEfU7'



def update_dop_text_file():
    Text.block_choose_time['buttons'] = [(button[0], f'time_{button[1]}') for button in buttons_list] + [Text.block_choose_time['buttons'][-1]]
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

buttons_list = {buttons_list}

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

def update_env_file():
    content = f"""TRACKING_BOT_TOKEN = '{TRACKING_BOT_TOKEN}'
GROUP_ID = '{GROUP_ID}'
USER_BOT = '{USER_BOT}'
USER_BOT_TOKEN = '{USER_BOT_TOKEN}'
CHANEL_LINK = '{CHANEL_LINK}'
LAVATOP = '{LAVATOP}'
LAVATOP_API = '{LAVATOP_API}'
CRYPTO = '{CRYPTO}'
CRYPTO_TOKEN = '{CRYPTO_TOKEN}'
"""
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(content)

def get_products_id(token):
    api = Lava.LavaTopAPI(token)
    products = api.get_products()
    if products:
        for item in products.json()['items']:
            for offer in item['offers']:
                print(offer['name'], offer['id'])
    else:
        print('Error get products')



update_dop_text_file()
update_env_file()
# get_products_id(LAVATOP_API)
