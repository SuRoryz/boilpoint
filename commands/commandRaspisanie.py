import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'расписание'

async def commandRaspisanie(event):

    await event.respond("раписание, ня")