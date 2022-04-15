import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql

key = 'социальные сети'

async def commandSocialMedia(event):

    await event.respond(SOCIAL_MEDIA)