import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'пространство'

async def commandP(event):

    await event.respond(P1)
    await event.respond(P2)
    await event.respond(P3)
    await event.respond(P4)
    await event.respond(P5)