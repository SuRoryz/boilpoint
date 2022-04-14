import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *

async def commandStart(event):
    chat = event.chat_id
    
    #await client.send_message(chat, 'A single button, with "clk1" as data',
    #                buttons=Button.inline('Click me', b'clk1'))

    markup = event.client.build_reply_markup(
        [[Button.text(x)] for x in MENU_BUTTONS]
        )
    
    await event.respond("Добро пожаловать в точку кипения", buttons=markup)