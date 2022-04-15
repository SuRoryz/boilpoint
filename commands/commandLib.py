import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'библиотека'

async def commandLib(event):
    chat = event.chat_id

    markup = event.client.build_reply_markup(
        [[Button.text(x)] for x in MENU_BUTTONS["Библиотека"]]
        )
    
    await event.respond("Выберите действие", buttons=markup)