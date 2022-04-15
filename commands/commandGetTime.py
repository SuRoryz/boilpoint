import sys
sys.path.append("..")

from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from config import *
from sql import Sql
from json import dumps, loads
from gcalendar import GoogleCalendar
from collections import namedtuple

key = 'забронировать дату'

async def commandGetTime(event) -> None:   
    user = event.chat_id
    Cache = dumps({'type': 'command_get_time_1'})
    Sql.updateCache(user, "c1", Cache)
    Cache = dumps({})
    Sql.updateCache(user, "c3", Cache)

    await event.respond("Укажите желаемое время в формате дд.мм.гггг чч:мм-чч:мм\n(Пример: 15.04.2022 10:40-13:30")

async def proccForm(event, step, data_=None, e=False) -> None:
    user = event.chat_id
    step = step[-1]
    
    cache = Sql.getCache(user)
    
    if cache[0][3]:
        c3 = loads(cache[0][3])
        data = c3
    else:
        data = {}
    
    if step == '1':
        text = event.raw_text
        
        d, m, y = text[:2], text[3:5], text[6:10]
        start_t, end_t = text[11:16], text[17:22]
        
        data['date'] = {'datetime_s': f'{y}-{m}-{d}T{start_t}:00+03:00', 'datetime_e': f'{y}-{m}-{d}T{end_t}:00+03:00'}
        
        Cache = dumps({'type': 'command_get_time_2'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)

        print(data)
        
        buttons = [
            [Button.inline('Л', b'time_L'),
             Button.inline('МЛ', b'time_ML'),
             Button.inline('П', b'time_P')]
        ]
        
        await event.respond('Выберите пространство', buttons=buttons)
    
    elif step == '2':
        await event.edit("Проверяем доступность...")
        
        calendar = GoogleCalendar()

        event_s = datetime.strptime(data['date']['datetime_s'], '%Y-%m-%dT%H:%M:00+03:00')
        event_e = datetime.strptime(data['date']['datetime_e'], '%Y-%m-%dT%H:%M:00+03:00')
        
        Range = namedtuple('Range', ['start', 'end'])
        r1 = Range(start=event_s, end=event_e)        
        events = calendar.get_events_list()
        
        p = data_.decode('utf-8')
        p = p[p.index('_')+1:][0]
        
        e2r = {
            'М': 'M',
            'Л': 'L',
            'П': 'P'
        }
        
        for _event in events:
            print(p, _event[2][1])
            if e2r[_event[2][1]] == p:  
                
                r2 = Range(start=datetime.strptime(_event[0], '%Y-%m-%dT%H:%M:00+03:00'), end=datetime.strptime(_event[1], '%Y-%m-%dT%H:%M:00+03:00'))
                delta = ((r1.start < r2.end) and (r2.start < r1.end))
                
                if delta:
                    Cache = dumps({'type': 'command_get_time_1'})
                    Sql.updateCache(user, "c1", Cache)
                    Cache = dumps({})
                    Sql.updateCache(user, "c3", Cache)
                    
                    await event.edit("Извините, но на это время в данном пространстве уже есть мероприятие. Попробуйте выбрать другое время или простратсво")
                    return
        
        data["p"] = p
        data["more"] = "-"
        data["broad"] = "Нет"
        
        Cache = dumps({'type': 'command_get_time_3'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)
        
        await event.edit("Это время свободно! Укажите количество человек на мероприятии")
    
    elif step == '3':
        number = event.raw_text
        
        if not(number.isnumeric()):
            await event.edit('Укажите только число человек, учавствующих в мероприятии')
            return

        data['members'] = number
        
        Cache = dumps({'type': 'command_get_time_4'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)
        
        await event.respond("Укажите название мероприятия.")
    
    elif step == '4':
        name = event.raw_text

        data['name'] = name
        
        Cache = dumps({'type': 'command_get_time_5'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)
        
        await event.respond("Укажите ФИО")
    
    elif step == '5':
        FIO = event.raw_text

        data['FIO'] = FIO
        
        Cache = dumps({'type': 'command_get_time_6'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)
        
        await event.respond("Укажите номер телефона для связи")
    
    elif step == '6':
        number = event.raw_text

        data['number'] = number
        
        Cache = dumps({'type': 'command_get_time_7'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)
        
        await event.respond("Укажите описание мероприятия")
    
    elif step == '7':
        about = event.raw_text

        data['about'] = about
        
        Cache = dumps({'type': 'command_get_time_8'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)
        
        buttons = [
            [Button.inline('Что нужно для огранизвации', b'time_More'),
             Button.inline('Планируется трансляция', b'time_Broad')],
            [Button.inline('Готово', b'time_Done'),
             ]
        ]
        
        time_s = datetime.strptime(data['date']['datetime_s'], '%Y-%m-%dT%H:%M:00+03:00')
        time_e = datetime.strptime(data['date']['datetime_e'], '%Y-%m-%dT%H:%M:00+03:00')
        
        if time_s.strftime("%d") == time_e.strftime("%d"):
            str_time = f"{time_s.strftime('%d.%m.%Y %H:%M')}-{time_e.strftime('%H:%M')}"
        else:
            str_time = f"{time_s.strftime('%d.%m.%Y %H:%M')} - {time_e.strftime('%d.%m.%Y %H:%M')}"
            
        r2e = {
            'M': 'МЛ',
            'L': 'Л',
            'P': 'П'
        }
        
        await event.respond(f"Ваша анкета:\n{data['name']} - {data['members']} человек.\nПространство: {r2e[data['p']]}\nВремя: {str_time}\n\nПланируется трансляция: {data['broad']}\nЧто нужно для организации: {data['more']}\n\nОписание: {data['about']}\n\nНомер телефона: {data['number']}\nФИО: {data['FIO']}\n\nХотите указать дополнительные сведения?", buttons=buttons)
    
    elif step == '8':
        
        option = data_.decode('utf-8')
        
        if option == 'time_More':
            Cache = dumps({'type': 'command_get_time_9'})
            Sql.updateCache(user, "c1", Cache)
            Cache = dumps(data)
            Sql.updateCache(user, "c3", Cache)
            
            await event.edit("Укажите, что вам нужно для организации мероприятия.")
        
        elif option == "time_Broad":
            if data['broad'] == 'Нет':
                data['broad'] = 'Да'
            else:
                data['broad'] = 'Нет'
            
            Cache = dumps({'type': 'command_get_time_8'})
            Sql.updateCache(user, "c1", Cache)
            Cache = dumps(data)
            Sql.updateCache(user, "c3", Cache)
            
            buttons = [
                [Button.inline('Что нужно для огранизвации', b'time_More'),
                Button.inline('Планируется трансляция', b'time_Broad')],
                [Button.inline('Готово', b'time_Done'),
                ]
            ]
            
            time_s = datetime.strptime(data['date']['datetime_s'], '%Y-%m-%dT%H:%M:00+03:00')
            time_e = datetime.strptime(data['date']['datetime_e'], '%Y-%m-%dT%H:%M:00+03:00')
            
            if time_s.strftime("%d") == time_e.strftime("%d"):
                str_time = f"{time_s.strftime('%d.%m.%Y %H:%M')}-{time_e.strftime('%H:%M')}"
            else:
                str_time = f"{time_s.strftime('%d.%m.%Y %H:%M')} - {time_e.strftime('%d.%m.%Y %H:%M')}"
                
            r2e = {
                'M': 'МЛ',
                'L': 'Л',
                'P': 'П'
            }
            
            await event.edit(f"Ваша анкета:\n{data['name']} - {data['members']} человек.\nПространство: {r2e[data['p']]}\nВремя: {str_time}\n\nПланируется трансляция: {data['broad']}\nЧто нужно для организации: {data['more']}\n\nОписание: {data['about']}\n\nНомер телефона: {data['number']}\nФИО: {data['FIO']}\n\nХотите указать дополнительные сведения?", buttons=buttons)
        
        
        elif option == 'time_Done':
            await event.edit("Отправляем анкету...")
            
            calendar = GoogleCalendar()
            
            r2e = {
                'M': 'МЛ',
                'L': 'Л',
                'P': 'П'
            }
            
            event_ = calendar.create_event_dict(name=f"-{r2e[data['p']]}/{data['members']} {data['name']}",
                                               desc=f"Номер телефона: {data['number']}\nФИО: {data['FIO']}\n\nЧто нужно для организации: {data['more']}\nБудет трансляция: {data['broad']}\nОписание: {data['about']}\n\nПоставил бот. Бип-буп",
                                               start_date=data['date']['datetime_s'], end_date=data['date']['datetime_e'])
            
            calendar.create_event(event_)
            
            await event.edit("Готово! Вам позвонят для уточнения")
    
    elif step == '9':
        more = event.raw_text
        
        data['more'] = more
        
        Cache = dumps({'type': 'command_get_time_8'})
        Sql.updateCache(user, "c1", Cache)
        Cache = dumps(data)
        Sql.updateCache(user, "c3", Cache)
        
        buttons = [
            [Button.inline('Что нужно для огранизвации', b'time_More'),
             Button.inline('Планируется трансляция', b'time_Broad')],
            [Button.inline('Готово', b'time_Done'),
             ]
        ]
        
        time_s = datetime.strptime(data['date']['datetime_s'], '%Y-%m-%dT%H:%M:00+03:00')
        time_e = datetime.strptime(data['date']['datetime_e'], '%Y-%m-%dT%H:%M:00+03:00')
        
        if time_s.strftime("%d") == time_e.strftime("%d"):
            str_time = f"{time_s.strftime('%d.%m.%Y %H:%M')}-{time_e.strftime('%H:%M')}"
        else:
            str_time = f"{time_s.strftime('%d.%m.%Y %H:%M')} - {time_e.strftime('%d.%m.%Y %H:%M')}"
            
        r2e = {
            'M': 'МЛ',
            'L': 'Л',
            'P': 'П'
        }
        
        await event.respond(f"Ваша анкета:\n{data['name']} - {data['members']} человек.\nПространство: {r2e[data['p']]}\nВремя: {str_time}\n\nПланируется трансляция: {data['broad']}\nЧто нужно для организации: {data['more']}\n\nОписание: {data['about']}\n\nНомер телефона: {data['number']}\nФИО: {data['FIO']}\n\nХотите указать дополнительные сведения?", buttons=buttons)
    
            
            
        
        
    
        