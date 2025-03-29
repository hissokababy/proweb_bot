import os
from dotenv import load_dotenv

load_dotenv()
# TOKEN = os.getenv('TOKEN')
TOKEN = '7886050826:AAG4_E2bZE85JIovV0gu8ONLY98ciW6XUYo'

CONTACT_GROUP_ID = os.getenv('CONTACT_GROUP_ID')

URL = 'https://8619-192-166-230-205.ngrok-free.app/getpost/'

TELEGRAM_API_URL = f'https://api.telegram.org/{TOKEN}/'
