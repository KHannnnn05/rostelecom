from aiogram import types
from bot import dp
from aiogram.dispatcher.filters import Text
from config import db, sv_id, admin_id
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserState(StatesGroup):
    username: str = State()

@dp.message_handler(Text(equals='Добавить сотрудника'))
async def new_staff(message: types.Message):
    if message.chat.id == (int(sv_id)) or message.chat.id == (int(admin_id)):
        await message.reply('Отправьте пожалуйста username нового сотрудника,' + \
                            'и я вам создам ссылку для добавления нового сотруника' + \
                            'username отправляйте без знака "собачка" (@)', reply_markup=types.ReplyKeyboardRemove())
        await UserState.username.set()
    else:
        await message.reply('Ты кто такой, чтобы добавлять новых сотрудников?')


@dp.message_handler(state=UserState.username)
async def get_id(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)

    username = await state.get_data()
    telegram_username = str(username['username'])
    returning_id = db.add_new_staff(telegram_username)
    link = f'https://t.me/sz_rtk_bot?start={returning_id}'
    await message.answer(f"```{link}```", parse_mode='Markdown')
    await state.finish()

