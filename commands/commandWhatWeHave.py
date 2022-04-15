import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'требования к мероприятиям'

async def commandWhatWeHave(event):

    await event.respond(REQS)
    await event.respond(REQS1)