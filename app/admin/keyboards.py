from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить', callback_data='confirm')],
    [InlineKeyboardButton(text='Не отправлять', callback_data='reset')]
])