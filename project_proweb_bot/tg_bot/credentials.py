import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
CONTACT_GROUP_ID = os.getenv('CONTACT_GROUP_ID')

URL = 'https://02c8-192-166-230-205.ngrok-free.app/getpost/'

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'
