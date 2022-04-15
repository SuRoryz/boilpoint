import sys
sys.path.append("..")

from telethon import TelegramClient, events
from telethon.tl.custom import Button
import config
from sheets import Sheets
from random import randint

key = 'случайная книга'

async def commandFindRandomBook(event) -> None:
    
    buttons = [[]]
    counter = 0
    line = 0
    
    print(config.CATEGORIES)
    
    for ctg in config.CATEGORIES:
        buttons[line].append(Button.inline(ctg, bytes(ctg, "UTF-8")))
        counter += 1
        
        if counter == 3:
            line += 1
            counter = 0
            buttons.append([])
    
    await event.respond("Какую категорию вы хотите?", buttons=buttons)

async def findBook(event) -> None:
    
    text = event.data.decode('utf-8')
    await event.edit('Выбираем случайную книгу...')
    
    sh = Sheets()
    table = sh.getTable()
    sheet = table.worksheet(value=1)
    
    find_area = sheet.get_all_records()
    results = []
    
    for row in find_area:
        if row["Категория"].lower() == text.lower():
            results.append(row)
    
    r = randint(0, len(results)-1) if len(results) > 1 else 0
    
    book = results[r]
    book = [book[key] for key in book.keys()]
    
    await event.respond(f'📕 **{book[0]}**\nАвтор: {book[1]}\nКатегория: {book[2]}\nМесто на полке: {book[3]}\nАннотация: {book[4]}\nОценка: {book[5]}\n\n', file=f"photos/{book[6]}")
    
    
    