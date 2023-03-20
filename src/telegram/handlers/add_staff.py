from aiogram import types
from bot import dp
from config import db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserState(StatesGroup):
    username: str = State()

@dp.message_handler(commands=['add_staff'])
async def new_staff(message: types.Message):
    await message.reply('Отправьте пожалуйста username нового сотрудника,' + \
                        'и я вам создам ссылку для добавления нового сотруника' + \
                        'username отправляйте без знака "собачка" (@)')
    await UserState.username.set()

@dp.message_handler(state=UserState.username)
async def get_id(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)

    username = await state.get_data()
    telegram_username = str(username['username'])
    returning_id = db.add_new_staff(telegram_username)
    link = f'https://t.me/sz_rtk_bot?start={returning_id}'
    await message.answer(link)
    await state.finish()

