import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'как зарегистрировать мероприятие на leader-id.ru'

async def commandIOrg(event):

    await event.respond(IORG)