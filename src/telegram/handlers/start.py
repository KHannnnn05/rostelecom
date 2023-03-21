from aiogram import types
from bot import dp, bot
from config import sv_id, db
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class InfoState(StatesGroup):
    full_name: str = State()
    phone_number: int = State()
    telegram_id: int = State()
    career_start_date: str = State()

sv_kb = [
    [types.KeyboardButton(text='Добавить сотрудника')],
    [types.KeyboardButton(text='Показать результат')],
    ]

start_sv_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, keyboard=sv_kb)

all_kb = [[(types.KeyboardButton(text='Новая заявка'))],]

start_all_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=all_kb)

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):

    if db.get_staff_id(message.chat.id):
        now = int(datetime.datetime.now().time().strftime('%H'))
        full_name = db.get_full_name(message.chat.id).split()
        full_name = (' '.join(full_name[1:3]))
        if now <= 12:
            await message.reply(f'Доброе утро, {full_name}!', reply_markup=start_all_kb)
        elif now <= 19:
            await message.reply(f'Добрый день, {full_name}!', reply_markup=start_all_kb)
        else:
            await message.reply(f'Добрый вечер, {full_name}!', reply_markup=start_all_kb)
    elif message.chat.id == sv_id:
        now = int(datetime.datetime.now().time().strftime('%H'))
        full_name = 'Артур'
        if now <= 12:
            await message.reply(f'Доброе утро, {full_name}!', reply_markup=start_sv_kb)
        elif now <= 19:
            await message.reply(f'Добрый день, {full_name}!', reply_markup=start_sv_kb)
        else:
            await message.reply(f'Добрый вечер, {full_name}!', reply_markup=start_sv_kb)
    elif (len(message.text.split())) == 2:
        await message.reply('Добро пожаловать в 6-ю команду!\n' + \
                            'Для начала вам необходимо будет заполнить анкету\n' + \
                            'Введите полностью ваше ФИО.\n' + \
                            'Например: Иванов Иван Иванович\n')
        await InfoState.full_name.set()
    else:
        await message.answer('Ты кто такой?')

@dp.message_handler(state=InfoState.full_name)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить номер", request_contact=True))
    await message.answer('Приятно познакомиться!\n' + \
                         'Остался последний шаг, отправьте пожалуйста ваш номер нажав на кнопку', reply_markup=keyboard)
    await InfoState.phone_number.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=InfoState.phone_number)
async def save_end_data(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number, 
                            telegram_id=int(message.chat.id),
                            career_start_date='01.01.2023')
    data = await state.get_data()
    db.add_new_staff_info(data)
    await message.reply('Отлично,\nВсе данные сохранены!\nВам удачи, и побольше заявок!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(reply_markup=start_all_kb)
    await bot.send_message(chat_id=sv_id, text='В вашу команду добавлен новый сотрудник!\n\n' + \
                                        f'ФИО: *{data["full_name"]}*\nНомер: ```{data["phone_number"]}```', parse_mode='Markdown')
    await state.finish()



