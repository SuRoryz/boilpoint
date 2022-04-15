import sys
sys.path.append("..")

from telethon.tl.custom import Button
import config
from sql import Sql
from sheets import Sheets
from json import dumps, loads

key = 'найти книгу'

async def commandFindBook(event):
    user = event.chat_id
    Cache = dumps({'type': 'command_find_book'})
    Sql.updateCache(user, "c1", Cache)
    
    await event.respond("Я могу найти для вас книгу в точке кипения. Напишите мне её название или автора")
    
async def findBook(event, by="title", default=True):
    
    if not(default):
        user = event.chat_id
        cache = Sql.getCache(user)
        c2 = loads(cache[0][2])
        
        text = c2[0]
        await event.edit('Ищу...')

    else:
        text = event.raw_text.lower()
    
    sh = Sheets()
    table = sh.getTable()
    sheet = table.worksheet(value=1)
    
    find_area = sheet.get_all_records()

    msg = 'Что мне удалось найти:\n\n'
    counter = 0
    
    search_result = []
    buttons= [
            [Button.inline('По автору' if by in ['title', 'annot'] else 'По названию', b'author' if by in ['title', 'annot'] else b'title'),
             Button.inline('По аннотации' if by in ['title', 'author'] else 'По названию', b'annot' if by in ['title', 'author'] else b'title')],
        ]
    
    for row in find_area:
        f = 0
        if by == "title":
            if text in row["Название"].lower():
                counter += 1 
                f = 1     
        elif by == 'author':
            if text in row["Автор"].lower():
                counter += 1
                f = 1
        else:
            if text in row["Аннотация"].lower():
                counter += 1
                f = 1
    
        if f:
            row_ = [row[key] for key in row.keys()]

            print(row_)
            
            if counter < config.MAX_BOOK_ON_PAGE + 1:
                msg += f'📕 **{row_[0]}**\nАвтор: {row_[1]}\nКатегория: {row_[2]}\nМесто на полке: {row_[3]}\nПодробнее: /b_{row_[7]}\n\n'
            else:
                search_result.append(row_)

    if counter >= config.MAX_BOOK_ON_PAGE + 1 and len(search_result):
        buttons.insert(0, [Button.inline(f'Показать ещё {len(search_result)}', bytes(f'show_more!{by}', "UTF-8"))])
        
        Sql.updateCache(event.chat_id, "c2", dumps([text, search_result]))

    if msg == 'Что мне удалось найти:\n\n':
        msg = 'Ничего не найдено :('
    
    if default:
        await event.respond(msg, parse_mode='md', buttons=buttons)
    else:
        await event.edit(msg, parse_mode='md', buttons=buttons)
    
async def findMore(event, by='title'):
    user = event.chat_id
    cache = Sql.getCache(user)
    c2 = loads(cache[0][2])
    print(cache, c2)
    
    msg = 'Что мне удалось найти:\n\n'
    counter = 0
    
    buttons= [
            [Button.inline('По автору' if by in ['title', 'annot'] else 'По названию', b'author' if by in ['title', 'annot'] else b'title'),
             Button.inline('По аннотации' if by in ['title', 'author'] else 'По названию', b'annot' if by in ['title', 'author'] else b'title')],
        ]
    search_result = []
    
    for row_ in c2[1]:
        counter += 1
        
        print(row_)
        
        if counter < config.MAX_BOOK_ON_PAGE + 1:
            msg += f'📕 **{row_[0]}**\nАвтор: {row_[1]}\nКатегория: {row_[2]}\nМесто на полке: {row_[3]}\nПодробнее: /b_{row_[7]}\n\n'
        else:
            search_result.append(row_)
    
    if counter >= config.MAX_BOOK_ON_PAGE + 1 and len(search_result):
        buttons.insert(0, [Button.inline(f'Показать ещё {len(search_result)}', bytes(f'show_more!{by}', "UTF-8"))])
        
        Sql.updateCache(event.chat_id, "c2", dumps([c2[0], search_result]))
    
    await event.edit(msg, buttons=buttons)

async def aboutBook(event) -> None:
    book = event.raw_text[3:]
    
    sh = Sheets()
    table = sh.getTable()
    sheet = table.worksheet(value=1)
    
    row_ = sheet.get_values(f'A{int(book)+1}', f'G{int(book)+1}')[0]
    await event.respond(f'📕 **{row_[0]}**\nАвтор: {row_[1]}\nКатегория: {row_[2]}\nМесто на полке: {row_[3]}\nАннотация: {row_[4]}\nОценка: {row_[5]}\n\n', file=f"photos/{row_[6]}")