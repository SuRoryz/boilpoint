import config
import os
import importlib

from sheets import Sheets

def initCommands() -> dict:
    # Получаем модули комманд из папки commands
    modules: list = os.listdir('commands')
    commands: dict = dict()
    
    # Проходим через все py файлы и импортируем функцию команды
    # А так же её ключ
    for module in modules:
        if module == "__pycache__":
            continue
        
        module = module.strip('.py')
        
        module_module = importlib.import_module(f'commands.{module}')
        module_func = getattr(module_module, module)
        module_key = getattr(module_module, "key")
        
        commands[module_key] = module_func
    
    return commands

# Получаем данные из гугл таблицы
def initConfig() -> None:
    sh = Sheets()
    table = sh.getTable()
    
    wks = table.sheet1
    config.RULES = wks.cell('A2').value
    config.HOW_TO_USE = wks.cell('B2').value
    
    config.P1 = wks.cell('C2').value
    config.P2 = wks.cell('C3').value
    config.P3 = wks.cell('C4').value
    config.P4 = wks.cell('C5').value
    config.P5 = wks.cell('C6').value
    
    config.REQS = wks.cell('D2').value
    config.REQS1 = wks.cell('D3').value
    
    config.IMEM = wks.cell('E2').value
    config.SOCIAL_MEDIA = wks.cell('F2').value
    
    config.WE1 = wks.cell('G2').value
    config.WE2 = wks.cell('G3').value
    
    config.IORG = wks.cell('H2').value
    config.CATEGORIES = wks.get_col(10, include_tailing_empty=False)[1:]