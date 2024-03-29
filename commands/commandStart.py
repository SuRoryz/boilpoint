import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = '/start'

async def commandStart(event):
    chat = event.chat_id

    markup = event.client.build_reply_markup(
        [[Button.text(x)] for x in MENU_BUTTONS.keys()]
        )
    
    await event.respond("Добро пожаловать в точку кипения", buttons=markup)