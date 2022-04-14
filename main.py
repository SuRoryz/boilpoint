from telethon import TelegramClient, events
from telethon.tl.custom import Button
import os
import importlib

from config import *

client = TelegramClient(SESSION, APP_ID, APP_HASH)
client.start(bot_token=BOT_TOKEN)

# - - - - - HANDLERS - - - - -
@client.on(events.NewMessage)
async def message_handler(event) -> None:
    
    text: str = event.raw_text.lower()
    is_me: bool = event.message.out
    peer_id: int = event.chat_id

    if not(is_me):
        text = text.split() 

        if text[0][0] == '/':
            await COMMANDS[text[0].strip('/')](event)
        
        elif event.raw_text == '/start':
            return

@client.on(events.CallbackQuery)
async def inlineHandler(event):
    await event.edit('Thank you for clicking {}!'.format(event.data))

# - - - - - HANDLERS - - - - -

def initCommands() -> dict:
    modules: list = os.listdir('commands')
    commands: dict = dict()
    
    for module in modules:
        if module == "__pycache__":
            continue
        
        module = module.strip('.py')
        module_func = getattr(importlib.import_module(f'commands.{module}'), module)
        
        commands[module.strip("command").lower()] = module_func
    
    return commands

if __name__ == "__main__":
    COMMANDS = initCommands()
    print(COMMANDS)
    client.run_until_disconnected()