from aiogram import Router, F
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
    