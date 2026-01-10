from aiogram.fsm.state import State, StatesGroup

class Consultation(StatesGroup):
    name = State()
    request = State()
    date = State()


class Test(StatesGroup):
    question = State()