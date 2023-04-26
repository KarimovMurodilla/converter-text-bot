from aiogram.dispatcher.filters.state import State, StatesGroup


class Reg(StatesGroup):
	step1 = State()
	step2 = State()
	step3 = State()