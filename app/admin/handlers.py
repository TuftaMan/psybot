from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command

from app.admin.states import Newletter
import app.admin.keyboards as kb

class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [407125211, 1018237453]
    
admin = Router()

#Команда для сброса машины состояний
@admin.message(Admin(), Command('stop'))
async def stop_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Задача очищена')

#Команда для рассылки в личные сообщения пользователей
@admin.message(Admin(), Command('letter'))
async def newletter(message: Message, state: FSMContext):
    await state.set_state(Newletter.tg_id)
    await message.answer('Введите тг кому отправить сообщение')

@admin.message(Newletter.tg_id, Admin())
async def write_tg(message: Message, state: FSMContext):
    try:
        tg_id = int(message.text)
    except:
        await message.answer("Пожалуйста, введите числовой tg_id.")
        return
    await state.update_data(tg_id=tg_id)
    data = await state.get_data()
    await message.answer(f"Введите сообщение которое вы хотите отправить пользователю с tg_id - {data.get('tg_id')}")
    await state.set_state(Newletter.letter)

@admin.message(Newletter.letter, Admin())
async def write_letter(message: Message, state: FSMContext):
    await state.update_data(letter=message.text)
    data = await state.get_data()
    await message.answer(f"Сообщение которое вы хотите отправить:\n\n{data.get('letter')}", reply_markup=kb.confirm)

@admin.callback_query(Newletter.letter, F.data == 'confirm', Admin())
async def write_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer('')
    data = await state.get_data()
    tg_id = data.get('tg_id')
    letter = data.get('letter')
    await bot.send_message(chat_id=tg_id, text=f'Отвечаю на Ваш вопрос:\n\n{letter}')
    await state.clear()
    await callback.message.answer('Сообщение доставлено пользователю!')

@admin.callback_query(Newletter.letter, F.data == 'reset', Admin())
async def write_reset(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer('')
    await state.clear()
    await callback.message.answer('Задача очищена')