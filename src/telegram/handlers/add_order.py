from aiogram import types
from bot import dp, bot
from config import db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prettytable import PrettyTable
from aiogram.dispatcher.filters import Text


order_kb = InlineKeyboardMarkup(row_width=2)
but_1 = InlineKeyboardButton(text="Все верно!", callback_data='y')
but_2 = InlineKeyboardButton(text='Редактировать данные', callback_data='n')
order_kb.add(but_1, but_2)

add_kb = InlineKeyboardMarkup(row_width=3)
bbi_button = InlineKeyboardButton(text='ШПД', callback_data='bbi')
tv_button = InlineKeyboardButton(text='ТВ', callback_data='tv')
mvno_button = InlineKeyboardButton(text='МВНО', callback_data='mvno')
cctv_button = InlineKeyboardButton(text='ВН', callback_data='cctv')
ss_button = InlineKeyboardButton(text='УК', callback_data='ss')
add_kb.add(bbi_button, tv_button, mvno_button, cctv_button, ss_button)

class OrderState(StatesGroup):
    bbi: bool = State()
    tv: bool = State()
    mvno: bool = State()
    cctv: bool = State()
    ss: bool = State()

@dp.message_handler(Text(equals='Новая заявка'))
async def new_order(message: types.Message):
    await message.answer(reply_markup=types.ReplyKeyboardRemove())
    await message.reply('Поздравляю вас с новой заявкой!\n' + \
                        'Ввыберите услуги которые вы продали и после этого отправьте любое сообщение боту \n', reply_markup=add_kb)
    await OrderState.bbi.set()
    await OrderState.tv.set()
    await OrderState.mvno.set()
    await OrderState.cctv.set()
    await OrderState.ss.set()

@dp.callback_query_handler(lambda c: True, state=OrderState)
async def adder(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        data.setdefault('items', [])
        if callback_query.data not in data['items']:
            data['items'].append(callback_query.data)

@dp.message_handler(state=OrderState)
async def get_id(message: types.Message, state: FSMContext):
    global ubbi, utv, umvno, ucctv, uss
    data = await state.get_data()
    options = data.get('items')
    table = PrettyTable()
    if options:
        table.field_names = ['ШПД', 'ТВ', 'МВНО', 'ВН', 'УК']
        ubbi = 1 if 'bbi' in options else 0
        utv = 1 if 'tv' in options else 0
        umvno = 1 if 'mvno' in options else 0
        ucctv = 1 if 'cctv' in options else 0
        uss = 1 if 'ss' in options else 0
        table.add_row([ubbi, utv, umvno, ucctv, uss])
    print(table)
    await message.answer(f"Подтвердите данные:\n```{table}```", parse_mode='MarkdownV2', reply_markup=order_kb)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'n')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите пожалуйста данные заново', reply_markup=add_kb)
    await OrderState.bbi.set()
    await OrderState.tv.set()
    await OrderState.mvno.set()
    await OrderState.cctv.set()
    await OrderState.ss.set()

@dp.callback_query_handler(lambda c: c.data == 'y')
async def yes(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    db.add_new_order(telegram_id=callback_query.from_user.id, bbi=ubbi, tv=utv, mvno=umvno, cctv=ucctv, ss=uss)
    await bot.send_message(callback_query.from_user.id, "Информация обновлена")