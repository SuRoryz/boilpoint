import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'организовать мероприятие'

async def commandOrganization(event):
    chat = event.chat_id

    markup = event.client.build_reply_markup(
        [[Button.text(x)] for x in MENU_BUTTONS["Организовать мероприятие"]]
        )
    
    await event.respond("Выберите действие", buttons=markup)