from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='О психологе', callback_data='about')],
    [InlineKeyboardButton(text='С какими запросами я работаю', callback_data='my_requests')],
    [InlineKeyboardButton(text='Записаться на консультацию', callback_data='consultation')],
    [InlineKeyboardButton(text='Подготовка к первой сессии', callback_data='first_session')],
    [InlineKeyboardButton(text='Нужна ли мне помощь?', callback_data='test')],
    [InlineKeyboardButton(text=' Частые вопросы', callback_data='questions')],
    [InlineKeyboardButton(text='Связаться лично', callback_data='contacts')],
    [InlineKeyboardButton(text='Стоимость моих услуг', callback_data='pricelist')],
])


back_to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
])


start_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать тест', callback_data='start_test')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
])

after_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записаться на консультацию', callback_data='consultation')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
])

async def answer_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Совсем не было', callback_data='ans_0')],
        [InlineKeyboardButton(text='Несколько дней', callback_data='ans_1')],
        [InlineKeyboardButton(text='Больше половины дней', callback_data='ans_2')],
        [InlineKeyboardButton(text='Почти каждый день', callback_data='ans_3')],
        [InlineKeyboardButton(text='Прервать тест', callback_data='back_to_main')],
    ])

