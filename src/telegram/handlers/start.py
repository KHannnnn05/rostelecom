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


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    now = int(datetime.datetime.now().time().strftime('%H'))
    print(message)
    if now <= 12:
        await message.reply(f'Доброе утро, {message.chat.first_name} {message.chat.last_name}!')
    elif now <= 19:
        await message.reply(f'Добрый день, {message.chat.first_name} {message.chat.last_name}!')
    else:
        await message.reply(f'Добрый вечер, {message.chat.first_name} {message.chat.last_name}!')
    if (len(message.text.split())) == 2:
        await message.reply('Добро пожаловать в 6-ю команду!\n' + \
                            'Для начала вам необходимо будет заполнить анкету\n' + \
                            'Введите полностью ваше ФИО.\n' + \
                            'Например: Иванов Иван Иванович\n')
        await InfoState.full_name.set()

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
    await message.answer('Отлично,\nВсе данные сохранены!\nВам удачи, и побольше заявок!')
    await bot.send_message(chat_id=sv_id, text='В вашу команду добавлен новый сотрудник!\n\n' + \
                                        f'ФИО: *{data["full_name"]}*\nНомер: ```{data["phone_number"]}```', parse_mode='Markdown')
    await state.finish()



