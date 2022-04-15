import config
from sql import Sql
from json import loads
from commands import commandFindBook, commandFindRandomBook, commandGetTime

async def handleNotCommand(event) -> None:
    user = event.chat_id
    
    if event.raw_text[0:2] ==  "/b":
        await commandFindBook.aboutBook(event)
        return
    
    cache = Sql.getCache(user)
    c1 = loads(cache[0][1])
    
    if c1['type'] == 'command_find_book':
        await commandFindBook.findBook(event)
    
    if c1['type'] in ['command_get_time_1', 'command_get_time_3', 'command_get_time_4', 'command_get_time_5', 'command_get_time_6', 'command_get_time_7', 'command_get_time_9']:
        await commandGetTime.proccForm(event, c1['type'])

async def handleInlineCommand(event) -> None:
    if event.data.decode("UTF-8").split('!')[0] == "show_more":
        by = event.data.decode("UTF-8").split('!')[1]
        await commandFindBook.findMore(event, by=by)
        return
    
    elif event.data in [b"author", b'annot', b'title']:
        by = event.data.decode("UTF-8")
        await commandFindBook.findBook(event, by=by, default=False)
    
    elif event.data.decode("UTF-8") in config.CATEGORIES:
        await commandFindRandomBook.findBook(event)
    
    elif event.data in [b'time_L', b'time_ML', b'time_P']:
        await commandGetTime.proccForm(event, 'command_get_time_2', event.data)
    
    elif event.data in [b'time_More', b'time_Broad', b'time_Done']:
        await commandGetTime.proccForm(event, 'command_get_time_8', event.data)
        
    #await event.edit('Thank you for clicking {}!'.format(event.data))