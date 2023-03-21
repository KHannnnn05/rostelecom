from aiogram import types
from bot import dp 
from config import db
from prettytable import PrettyTable


@dp.message_handler(commands=['get_rezult'])
async def rezult(message: types.Message):
    table = PrettyTable()
    if db.get_rezult():
        table.field_names = ['ФИО агента', 'ШПД', 'ТВ', 'МВНО', 'ВН', 'УК']
        for i in db.get_rezult():
            table.add_row(i)
    print(table)
    await message.reply(f'Результат команды за сегодня:\n\n`{table}`', parse_mode='MarkdownV2')
