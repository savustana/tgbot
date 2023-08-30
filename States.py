from aiogram.dispatcher.filters.state import StatesGroup, State

class States(StatesGroup):
    begin = State()
    today = State()
    choose = State()
    add = State()
