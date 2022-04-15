import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'как организовать мероприятие'

async def commandHowToUse(event):

    await event.respond(HOW_TO_USE)