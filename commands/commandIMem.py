import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'участникам'

async def commandIMem(event):

    await event.respond(IMEM)