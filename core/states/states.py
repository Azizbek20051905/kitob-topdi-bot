from aiogram.fsm.state import State, StatesGroup

class GetChannel_data(StatesGroup):
    name = State()
    link = State()

class GetAds_data(StatesGroup):
    name = State()
    link = State()

class ForwardMessage(StatesGroup):
    id = State()

class MoviesData(StatesGroup):
    name = State()
    part = State()
    size = State()
    file = State()

class MessageNext(StatesGroup):
    model = State()
    
