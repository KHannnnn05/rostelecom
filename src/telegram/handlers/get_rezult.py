from aiogram import types
from bot import dp 
from config import db, sv_id, admin_id
from prettytable import PrettyTable
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(equals='Показать результат'))
async def rezult(message: types.Message):
    if message.chat.id == (int(sv_id) | int(admin_id)):
        table = PrettyTable()
        if db.get_rezult():
            table.field_names = ['ФИО агента', 'ШПД', 'ТВ', 'МВНО', 'ВН', 'УК']
            for i in db.get_rezult():
                table.add_row(i)
        print(table)
        await message.reply(f'Результат команды за сегодня:\n\n`{table}`', parse_mode='MarkdownV2', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply('Ты кто такой, чтобы смотреть отчеты?')
