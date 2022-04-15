from telethon import TelegramClient, events

from sql import Sql
from handleNotCommand import handleNotCommand, handleInlineCommand

from config import *
from Inits import *

client = TelegramClient(SESSION, APP_ID, APP_HASH)
client.start(bot_token=BOT_TOKEN)

# - - - - - EVENT HANDLERS - - - - -
@client.on(events.NewMessage)
async def message_handler(event) -> None:
    
    text: str = event.raw_text.lower()
    is_me: bool = event.message.out
    peer_id: int = event.chat_id

    if not(is_me):
        # Добавляем пользователя в таблицу для кеша, если его там нет
        # И заодно кешируем это в памяти, чтоб не обращаться постоянно к дб
        if peer_id not in CACHED:
            Sql.setUpUser(peer_id)
            CACHED.append(peer_id)
        
        if text in COMMANDS:    
            await COMMANDS[text](event)
 
        else:
            await handleNotCommand(event)


client.add_event_handler(handleInlineCommand, events.CallbackQuery)

# - - - - - EVENT HANDLERS - - - - -
    
if __name__ == "__main__":
    initConfig()
    COMMANDS = initCommands()
    
    Sql.setUp()
    client.run_until_disconnected()