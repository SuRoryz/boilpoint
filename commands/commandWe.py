import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'команда'

async def commandWe(event):

    await event.respond(WE1)
    await event.respond(WE2)