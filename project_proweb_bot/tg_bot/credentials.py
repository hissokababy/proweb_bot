import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

URL = 'https://2bcc-192-166-230-205.ngrok-free.app/getpost/'

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'
