from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🧠 Обо мне', callback_data='about')],
    [InlineKeyboardButton(text='💬 С какими запросами я работаю', callback_data='my_requests')],
    [InlineKeyboardButton(text='📝 Записаться на консультацию', callback_data='consultation')],
    [InlineKeyboardButton(text='📊 Пройти тест', callback_data='test')],
    [InlineKeyboardButton(text='🧘🏼‍♀️ Практики', callback_data='practic')],
    [InlineKeyboardButton(text='💰 Стоимость', callback_data='pricelist')],
    [InlineKeyboardButton(text='📞 Контакты', callback_data='contacts')],
    [InlineKeyboardButton(text='💬 Задать свой вопрос', callback_data='your_question')]
])


back_to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data='back_to_main')]
])


start_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='▶️ Начать тест', callback_data='start_test')],
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data='back_to_main')]
])

after_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записаться на консультацию', callback_data='consultation')],
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data='back_to_main')]
])

async def answer_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Совсем не было', callback_data='ans_0')],
        [InlineKeyboardButton(text='Несколько дней', callback_data='ans_1')],
        [InlineKeyboardButton(text='Больше половины дней', callback_data='ans_2')],
        [InlineKeyboardButton(text='Почти каждый день', callback_data='ans_3')],
        [InlineKeyboardButton(text='Прервать тест', callback_data='back_to_main')],
    ])

start_writing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записаться на консультацию', callback_data='writing_to_consultation')],
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data='back_to_main')]
])

complete_conslt = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Отправить заявку', callback_data='send_info')],
    [InlineKeyboardButton(text='✏️ Изменить данные', callback_data='writing_to_consultation')],
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data='back_to_main')]
])

after_reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🧠 Обо мне', callback_data='about')],
    [InlineKeyboardButton(text='💬 С какими запросами я работаю', callback_data='my_requests')],
    [InlineKeyboardButton(text='📝 Записаться на консультацию', callback_data='consultation')],
    [InlineKeyboardButton(text='📊 Пройти тест', callback_data='test')],
    [InlineKeyboardButton(text='🧘🏼‍♀️ Практики', callback_data='practic')],
    [InlineKeyboardButton(text='💰 Стоимость', callback_data='pricelist')],
    [InlineKeyboardButton(text='📞 Контакты', callback_data='contacts')],
    [InlineKeyboardButton(text='💬 Задать свой вопрос', callback_data='your_question')]
])

practics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌙 Дыхание для сна', callback_data='practice_sleep')],
    [InlineKeyboardButton(text='⚡ Дыхание для концентрации', callback_data='practice_focus')],
    [InlineKeyboardButton(text='🎨 Арт-практика', callback_data='practice_art')],
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data='back_to_main')]
])

practics_emoji = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🙂 Стало спокойнее", callback_data="feeling_ok")],
    [InlineKeyboardButton(text="😐 Без изменений", callback_data="feeling_neutral")],
    [InlineKeyboardButton(text="😔 Стало сложнее", callback_data="feeling_hard")],
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data='back_to_main')]
])

