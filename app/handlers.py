import os
from dotenv import load_dotenv
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timezone

import app.keyboards as kb
from app.states import Consultation, Test, Question
from app.psy_test import QUESTIONS, get_result

client = Router()



@client.message(CommandStart(), lambda message: (datetime.now(timezone.utc) - message.date).total_seconds() < 10)
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здравствуйте 🌿\n\n"
    "Меня зовут Елена Нефедьева, я практический психолог.\n\n"
    "Это спокойное пространство, где вы можете без спешки "
    "познакомиться со мной, узнать о формате консультаций, "
    "пройти небольшой тест или записаться на индивидуальную встречу.\n\n"
    "Выбирайте то, что сейчас откликается 🤍",
                         reply_markup=kb.main,
                         parse_mode='Markdown'
                         )
    
@client.callback_query(F.data=='back_to_main')
async def cmd_back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.edit_text("Здравствуйте 🌿\n\n"
        "Меня зовут Елена Нефедьева, я практический психолог.\n\n"
        "Здесь вы можете спокойно познакомиться со мной, "
        "узнать о формате консультаций, пройти небольшой тест "
        "или записаться на индивидуальную встречу.\n\n"
        "Выбирайте то, что сейчас откликается — я рядом.",
                         reply_markup=kb.main,
                         parse_mode='Markdown'
                         )

@client.callback_query(F.data=='about')
async def cmd_about(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Меня зовут Елена Нефедьева, я практический психолог.\n\n"
    "В своей работе я создаю бережное и безопасное пространство, "
    "где можно честно говорить о чувствах, переживаниях и сложностях — "
    "без осуждения и давления.\n\n"
    "Мне важно не контролировать и не «исправлять», "
    "а быть рядом — как внимательный слушатель и союзник.\n\n"
    "Моя задача — помочь вам лучше понять себя и "
    "найти опору в собственной истории.",
                         reply_markup=kb.back_to_main,
                         parse_mode='Markdown'
                         )
    
@client.callback_query(F.data == 'my_requests')
async def cmd_my_requests(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Ко мне можно обратиться, если вы:\n\n"
    "— чувствуете тревогу или внутреннее напряжение\n"
    "— сталкиваетесь с эмоциональным выгоранием\n"
    "— переживаете сложности в отношениях\n"
    "— сомневаетесь в себе и своих решениях\n"
    "— чувствуете апатию или потерю мотивации\n"
    "— находитесь в жизненном кризисе или периоде перемен\n\n"
    "Если ваш запрос сложно сформулировать — это нормально.\n"
    "Мы можем делать это вместе, постепенно.", 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')

@client.callback_query(F.data == 'first_session')
async def cmd_first_session(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Первая сессия — это знакомство и совместное исследование 🌿\n\n"
    "Мы поговорим о том, что вас привело, "
    "о ваших ожиданиях и возможном формате работы.\n\n"
    "Специальной подготовки не требуется.\n"
    "Важно лишь ваше желание быть внимательным к себе.\n\n"
    "Вы сами решаете, о чём говорить и с какой глубиной.", 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')
    
@client.callback_query(F.data == 'test')
async def cmd_test(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Этот небольшой тест поможет мягко "
    "обратить внимание на ваше текущее эмоциональное состояние.\n\n"
    "Он не ставит диагноз и носит ознакомительный характер.\n\n"
    "Отвечайте так, как чувствуете — "
    "не задумываясь слишком долго 🌿", 
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
    await callback.message.edit_text("Связаться со мной можно здесь:\n\n"
    "Telegram: @Lenairk38\n"
    "VK: https://vk.com/id138880111\n\n"
    "Если удобнее — вы можете написать напрямую.", 
                                     reply_markup=kb.back_to_main,
                                     parse_mode='Markdown')
    
@client.callback_query(F.data == 'pricelist')
async def cmd_pricelist(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Стоимость услуг:\n\n"
    "— Первая консультация — Бесплатно\n"
    "— Индивидуальная сессия — от 3500 рублей\n\n"
    "Если у вас есть вопросы по формату или оплате — "
    "вы можете задать их в личном сообщении.", 
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
    await callback.message.edit_text("Консультация — это индивидуальная онлайн-встреча "
    "в спокойной и поддерживающей атмосфере 🌿\n\n"
    "Мы будем внимательно исследовать ваш запрос, "
    "чувства и мысли, а также искать возможные точки опоры.\n\n"
    "Первая встреча проходит бесплатно и носит ознакомительный характер.\n\n"
    "Если вы готовы сделать первый шаг — "
    "нажмите кнопку ниже.", reply_markup=kb.start_writing, parse_mode='Markdown')

@client.callback_query(F.data == 'writing_to_consultation')
async def cmd_writing_to_consultation(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(Consultation.name)
    await callback.message.edit_text('Давайте познакомимся 🙂\n\nНапишите, пожалуйста:\n— как вас зовут  \n— сколько вам лет', parse_mode='Markdown')

@client.message(Consultation.name)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Как с вами удобнее связаться? \n\nНапишите номер телефона или ник в Telegram.')
    await state.set_state(Consultation.contact)

@client.message(Consultation.contact)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer('Коротко опишите, что вас сейчас беспокоит.\n\nМожно без подробностей — ровно столько, сколько комфортно.')
    await state.set_state(Consultation.request)

@client.message(Consultation.request)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(request=message.text)
    await message.answer('В какую дату и время (по МСК) вам было бы удобно провести консультацию?')
    await state.set_state(Consultation.date)

@client.message(Consultation.date)
async def cmd_set_name(message: Message, state: FSMContext):
    await state.update_data(date=message.text)

    data = await state.get_data()
    name = data.get("name")
    contact = data.get('contact')
    request = data.get("request")
    date = data.get("date")

    await message.answer(f"Проверьте, пожалуйста, информацию 👇\n\nИмя: {name}\nКонтакт для связи: {contact}\nЗапрос: {request}\nДата: {date}\n\nЕсли всё верно — отправьте заявку.", reply_markup=kb.complete_conslt)

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
    
    await callback.message.edit_text("Спасибо за доверие 🌿\n\n"
        "Ваша заявка отправлена.\n"
        "Я свяжусь с вами в ближайшее время, "
        "чтобы подтвердить запись.", reply_markup=kb.after_reg, parse_mode='Markdown')
    
@client.callback_query(F.data == 'your_question')
async def cmd_your_question(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await state.set_state(Question.text)
    await callback.message.edit_text("Здесь вы можете задать любой вопрос 🌿\n\n"
    "О формате работы, консультациях, "
    "сомнениях или том, что сейчас волнует.\n\n"
    "Напишите ваш вопрос в этом чате — "
    "столько, сколько вам комфортно.", reply_markup=kb.back_to_main)
    
@client.message(Question.text)
async def cmd_get_question(message: Message, state: FSMContext, bot: Bot):
    question = message.text

    first_name = message.from_user.first_name
    username = message.from_user.username
    tg_id = message.from_user.id

    load_dotenv()

    await bot.send_message(
        chat_id=os.getenv("TG_CHAT_ID_RESERV"),
        text=(
            f"❓ Вопрос от пользователя\n\n"
            f"Имя: {first_name}\n"
            f"Username: @{username}\n"
            f"tg_id: {tg_id}\n\n"
            f"Вопрос:\n{question}"
        )
    )

    await state.clear()

    await message.answer(
        "Спасибо за вопрос 🌿\n\n"
        "Я постараюсь ответить вам в ближайшее время.",
        reply_markup=kb.after_reg
    )