from aiogram.fsm.state import State, StatesGroup

class Newletter(StatesGroup):
    tg_id = State()
    letter = State()

class ChannelMessage(StatesGroup):
    letter = State()