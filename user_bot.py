import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('USER_BOT_TOKEN')
print(token)