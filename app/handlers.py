import os
from dotenv import load_dotenv
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timezone

import app.keyboards as kb
from app.states import Consultation, Test
from app.psy_test import QUESTIONS, get_result

client = Router()



@client.message(CommandStart(), lambda message: (datetime.now(timezone.utc) - message.date).total_seconds() < 10)
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Hello',
                         reply_markup=kb.main,
                         parse_mode='Markdown'
                         )
    
@client.callback_query(F.data=='back_to_main')
async def cmd_back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.edit_text('Вы вернулись в главное меню', 
                                     reply_markup=kb.main,
                                     parse_mode='Markdown')

@client.callback_query(F.data=='about')
async def cmd_about(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Меня зовут Елена, я молодец', 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')
    
@client.callback_query(F.data == 'my_requests')
async def cmd_my_requests(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Я работаю с такими запросами', 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')

@client.callback_query(F.data == 'first_session')
async def cmd_first_session(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Для первой сессии нужно подготовиться или не нужно', 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')
    
@client.callback_query(F.data == 'test')
async def cmd_test(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('тест', 
                                     reply_markup=kb.start_test,
                                     parse_mode='Markdown')
    
@client.callback_query(F.data == 'questions')
async def cmd_questions(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Сейчас тут пусто, но должны быть вопросы', 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')
    
@client.callback_query(F.data == 'contacts')
async def cmd_contacts(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Меня можно найти тут:\nТГ:\nВк\nИнст:', 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')
    
@client.callback_query(F.data == 'pricelist')
async def cmd_pricelist(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Стоимость услуг:\nПервая консультация -\n Первый прием - \n', 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')

# Тестирование на психическое состояние
@client.callback_query(F.data == 'start_test')
async def cmd_start_test(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await state.set_state(Test.question)
    await state.update_data(index=0, score=0)
    await callback.message.edit_text(QUESTIONS[0], 
                                     reply_markup=await kb.answer_kb(),
                                     parse_mode='Markdown')
    
@client.callback_query(Test.question, F.data.startswith('ans_'))
async def cmd_process_test(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    data = await state.get_data()

    index = data['index']
    score = data['score']

    value = int(callback.data.split('_')[1])
    score += value
    index += 1

    if index >= len(QUESTIONS):
        await state.clear()
        await callback.message.edit_text(get_result(score), reply_markup=kb.after_test)
        return
    
    await state.update_data(index=index, score=score)
    await callback.message.edit_text(QUESTIONS[index], 
                                     reply_markup=await kb.answer_kb(),
                                     parse_mode='Markdown')

# запись на консультацию

@client.callback_query(F.data == 'consultation')
async def cmd_write_to_consultation(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Что представляет собой консультация?\nбла бла бла\n чтобы записаться нажмите кнопку ниже', 
                                     reply_markup=kb.start_writing,
                                     parse_mode='Markdown')

@client.callback_query(F.data == 'writing_to_consultation')
async def cmd_writing_to_consultation(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Consultation.name)
    await callback.message.edit_text('Давайте познакомимся, напишите как вас зовут и сколько вам лет', parse_mode='Markdown')

@client.message(Consultation.name)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('напишите ваш номер или ник в телеграме для связи', parse_mode='Markdown')
    await state.set_state(Consultation.contact)

@client.message(Consultation.contact)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer('Расскажите что вас беспокоит?', parse_mode='Markdown')
    await state.set_state(Consultation.request)

@client.message(Consultation.request)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(request=message.text)
    await message.answer('В какую дату и какое время по мск вам хотелось посетить сеанс', parse_mode='Markdown')
    await state.set_state(Consultation.date)

@client.message(Consultation.date)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(date=message.text)

    data = await state.get_data()
    name = data.get("name")
    contact = data.get('contact')
    request = data.get("request")
    date = data.get("date")

    await message.answer(f"Информация заполнена!\nИмя: {name}\nКонтакт для связи: {contact}\nЗапрос: {request}\nДата: {date}\nВы можете отправить информацию, и я свяжусь с вами.", reply_markup=kb.complete_conslt, parse_mode='Markdown')

@client.callback_query(F.data == 'send_info')
async def cmd_send_info(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer('')
    data = await state.get_data()
    name = data.get("name")
    contact = data.get('contact')
    request = data.get("request")
    date = data.get("date")
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    tg_id = callback.from_user.id
    load_dotenv()
    await bot.send_message(chat_id=os.getenv('TG_CHAT_ID'), text=f'Заявка от @{username}, Имя - {first_name}, tg_id - {tg_id}\n\nЗаявка на консультацию:\n'
                                      f'Имя: {name}\n'
                                      f'Контакт для связи: {contact}\n'
                                      f'Запрос: {request}\n'
                                      f'Дата: {date}')
    
    await callback.message.edit_text('Информация направлена Елене!', reply_markup=kb.after_reg, parse_mode='Markdown')