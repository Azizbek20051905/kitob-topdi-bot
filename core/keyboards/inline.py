from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from core.utils.callbackdata import AdminPanel, DeleteChannel, AddSaved, DeleteSaved, SelectedBooks, Statistic

from core.settings import settings
from core.db_api.db import all_ads, all_channels, get_checkbox, all_books, get_saveds_books_id
import random

# def client_user_btn():
#     keyboard = InlineKeyboardBuilder()

#     keyboard.button(text='🔎Barcha kinolar',  switch_inline_query_current_chat="")
#     keyboard.button(text="📂Saqlangan kinolar", switch_inline_query_current_chat="saved")
    
#     ads = all_ads()
#     if ads:
#         rand = random.choice(ads)
#         print()
#         print(rand)
#         print()
#         keyboard.button(text=f"{rand['name']}", url=f"{rand['link']}")
    
#     keyboard.button(text="Botni guruhga qo'shish", url=f'https://t.me/Kinochi_aka_bot?startgroup=true')
#     keyboard.button(text="Botni kanalga qo'shish", url=f'https://t.me/Kinochi_aka_bot?startchannel=true')
#     keyboard.adjust(1, 1, 1, 2)
    
#     return keyboard.as_markup()

def adminpanel_btn(model):
    keyboards = InlineKeyboardBuilder()

    keyboards.button(text="📊Statistika", callback_data=AdminPanel(model='statistic'))
    keyboards.button(text="📢Kanallar", callback_data=AdminPanel(model='channels'))
    keyboards.button(text="📝Xabar yuborish", callback_data=AdminPanel(model=model))
    keyboards.button(text="📚Kitob qo'shish", callback_data=AdminPanel(model='books'))
    keyboards.button(text="➕Reklama qo'shish", callback_data=AdminPanel(model='add_ads'))
    keyboards.button(text="➖Reklama o'chirish", callback_data=AdminPanel(model='del_ads'))
    keyboards.button(text="🔼", callback_data=AdminPanel(model='clear'))

    # keyboards.adjust(1)
    keyboards.adjust(2, 1, 1, 2, 1)

    return keyboards.as_markup()

def channel_btn():
    keyboards = InlineKeyboardBuilder()

    keyboards.button(text="➕Kanal qo'shish", callback_data=AdminPanel(model='add_channel'))
    keyboards.button(text="➖Kanal o'chirish", callback_data=AdminPanel(model='del_channel'))

    # if all_channels():
    is_true = get_checkbox()
    if is_true['is_true']:
        keyboards.button(text="✅Majburiy a'zolik|Yoqilgan", callback_data=AdminPanel(model='off_channel'))
    else:
        keyboards.button(text="❌Majburiy a'zolik|O'chirilgan", callback_data=AdminPanel(model='on_channel'))

    keyboards.button(text="🔙Orqaga", callback_data=AdminPanel(model='admin_panel'))
    keyboards.adjust(2, 1, 1)

    return keyboards.as_markup()

def del_channel_btn():
    keyboards = InlineKeyboardBuilder()

    channels = all_channels()
    if channels:
        for channel in channels:
            keyboards.button(text=channel['name'], callback_data=DeleteChannel(model='delete_channel', id=channel['id']))

    keyboards.button(text="🔙Orqaga", callback_data=AdminPanel(model='channels'))
    keyboards.adjust(2)

    return keyboards.as_markup()

def get_back_btn(model):
    keyboards = InlineKeyboardBuilder()
    keyboards.button(text="🔙Orqaga", callback_data=AdminPanel(model=model))
    keyboards.adjust(1)
    return keyboards.as_markup()

def books_btn():
    keyboards = InlineKeyboardBuilder()

    keyboards.button(text="➕Kitob qo'shish", callback_data=AdminPanel(model='add_book'))
    keyboards.button(text="➖Kitob o'chirish", callback_data=AdminPanel(model='del_book'))

    keyboards.button(text="🔙Orqaga", callback_data=AdminPanel(model='admin_panel'))
    keyboards.adjust(2, 1)

    return keyboards.as_markup()

def del_book_btn(data, model, go_back):
    keyboards = InlineKeyboardBuilder()

    movies = data
    print(movies)
    if movies:
        for movie in movies:
            print(movie)
            keyboards.button(text=movie['name'], callback_data=DeleteChannel(model=model, id=movie['id']))

    keyboards.button(text="🔙Orqaga", callback_data=AdminPanel(model=go_back))
    keyboards.adjust(1)

    return keyboards.as_markup()


def users_btn(data, user_id):
    keyboards = InlineKeyboardBuilder()

    keyboards.button(text='🔎Barcha Kitoblar',  switch_inline_query_current_chat="")
    keyboards.button(text="📂Saqlangan Kitoblar", switch_inline_query_current_chat="saved")
    results = get_saveds_books_id(users_id=user_id, book_id=data['id'])

    if results:
        keyboards.button(text="✅Saqlangan", callback_data=DeleteSaved(model='del_save', saved_id=int(results['id']), movie_id=int(data['id'])))
    else:
        keyboards.button(text="✔️Saqlash", callback_data=AddSaved(model='add_save', id=int(data['id']), user_id=str(user_id)))
    
    ads = all_ads()
    if ads:
        rand = random.choice(ads)
        keyboards.button(text=f"{rand['name']}", url=f"{rand['link']}")
    
    keyboards.adjust(2, 1, 1)

    return keyboards.as_markup()

def sub_channel_keyboard():
    keyboards = InlineKeyboardBuilder()
    
    channels = all_channels()
    if channels:
        for channel in channels:
            keyboards.button(text=f"{channel['name']}", url=f"{channel['link']}")

    keyboards.button(text="Tasdiqlash✅", callback_data=AdminPanel(model='checksub'))
    # keyboards.button(text="Tasdiqlash✔", callback_data=DeleteMessage(model='delete'))
    keyboards.adjust(1)
    return keyboards.as_markup()


def status_message_btn(play, model, message_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=play, callback_data=Statistic(model=model, id=message_id))
    keyboard.button(text="Yangilash🔄", callback_data=AdminPanel(model='update'))
    keyboard.button(text="O'chirish🗑", callback_data=AdminPanel(model='delete_status'))
    keyboard.button(text="🔙Orqaga", callback_data=AdminPanel(model='admin_panel'))

    keyboard.adjust(1)

    return keyboard.as_markup()


# def search_books_btn(data):
#     keyboards = InlineKeyboardBuilder()

#     for book in data:
#         keyboards.button(text=book['name'], callback_data=SelectedBooks(model='sel_bk', id=book['id']))

#     keyboards.button(text="⬅️", callback_data=AdminPanel(model='prev'))
#     keyboards.adjust(1)
#     keyboards.button(text="❌", callback_data=AdminPanel(model='del_message'))
#     keyboards.button(text="➡️", callback_data=AdminPanel(model='next'))
    

#     return keyboards.as_markup()
def search_books_btn(data, text, page=0):
    keyboards = InlineKeyboardBuilder()
    start_index = page * 10
    end_index = start_index + 10
    for i in range(start_index, min(end_index, len(data))):
        keyboards.button(text=data[i]['name'], callback_data=SelectedBooks(model='sel_bk', id=data[i]['id'], name=text))
    

    if page > 0:
        keyboards.button(text="⬅️Orqaga", callback_data=SelectedBooks(model='prev', id=page-1, name=text))
    if end_index < len(data):
        keyboards.button(text="➡️Keyingi", callback_data=SelectedBooks(model='next', id=page+1, name=text))

    keyboards.adjust(1)
    return keyboards.as_markup()
    

def book_type(id):
    keyboards = InlineKeyboardBuilder()

    keyboards.button(text="Audio format", callback_data=SelectedBooks(model='audio', id=id, name="audio"))
    keyboards.button(text="Kitob format", callback_data=SelectedBooks(model='document', id=id, name="document"))
    
    keyboards.adjust(2, 1)

    return keyboards.as_markup()

def next_prev_btn():
    keyboards = InlineKeyboardBuilder()

    
    keyboards.adjust(1)

    return keyboards.as_markup()