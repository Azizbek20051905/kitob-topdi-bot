import asyncio
from datetime import datetime, timedelta
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from core.settings import settings
from core.utils.callbackdata import AdminPanel, DeleteChannel, AddSaved, DeleteSaved, SelectedBooks
from core.keyboards.inline import (channel_btn, adminpanel_btn, del_channel_btn,
                                   get_back_btn, books_btn, del_book_btn, book_type, search_books_btn,
                                   users_btn, status_message_btn)
from core.db_api.db import (delete_channel, search_book, update_channel_details, all_channels, 
                            update_checkbox, all_books, delete_book_name_id, delete_books_id, all_ads, 
                            delete_ads, insert_saved, get_book_name_details, delete_saved)
# from core.settings import CheckSub
from core.states.states import ForwardMessage, MoviesData, GetChannel_data, GetAds_data, MessageNext
from core.config import set_global_var, global_var
from core.handlers.basic import user_views, answer_users
import uuid

sending_messages = True
send_answer_messages = {}


async def selected_books_btn(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: SelectedBooks):
    book_name_id = callback_data.id

    btn = book_type(id=book_name_id)
    await call.message.answer(text="Kitob turini tanlang: ", reply_markup=btn)

async def selected_audio(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: SelectedBooks):
    data = get_book_name_details(book_id=callback_data.id, types='audio')

    if data:
        for audio in data:
            await call.message.answer_audio(audio=str(audio['file']), caption=f"Kitob: {audio['name']}\nQism: {audio['part']}\nHajmi: {audio['size']}")
    else:
        await call.message.answer(text="Audio kitob topilmadi")
        await call.answer(text="Audio kitob topilmadi", show_alert=True)

async def selected_documents(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: SelectedBooks):
    data = get_book_name_details(book_id=callback_data.id, types='document')

    if data:
        for book in data:
            await call.message.answer_document(document=book['file'], caption=f"Kitob: {book['name']}\nQism: {book['part']}\nHajmi: {book['size']}")
    else:
        await call.message.answer(text="E-kitob topilmadi", disable_notification=True)
        await call.answer(text="E-kitob topilmadi", show_alert=True)


async def selected_channel(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    print()
    print("yana: ", global_var)
    print()
    await bot.edit_message_text(text="Kanallar", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=channel_btn())
    # await call.message.answer(text="Kanallar", reply_markup=channel_btn())
    
async def selected_admin_panel(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(text="Admin panel", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=adminpanel_btn(model='xabar'))

async def selected_del_channel(call: CallbackQuery, bot: Bot, callback_data: AdminPanel):
    await bot.edit_message_text(text="Kanallarni o'chirish uchun ustiga birmarta bosish kifoya:", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=del_channel_btn())
    # await call.message.answer(text="Kanallar", reply_markup=channel_btn())

async def deleted_channels(call: CallbackQuery, bot: Bot, callback_data: DeleteChannel):
    result = delete_channel(channel_id=callback_data.id)
    print(result)
    
    await bot.edit_message_text(text="Kanallarni o'chirish uchun ustiga birmarta bosish kifoya:", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=del_channel_btn())
    await call.message.answer(text="Kanal o'chirildi!")
    # await call.message.answer(text="Kanallar", reply_markup=channel_btn())

async def on_channels(call: CallbackQuery, bot: Bot, callback_data: AdminPanel):
    # await call.answer(text="Kanallar")
    if callback_data.model == 'on_channel':
        update_checkbox(is_true = True)
        print("on_channel")
        
        btn = channel_btn()
        await bot.edit_message_text(text="Kanallar", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=btn)
        # await call.answer(text="Kanallar", reply_markup=btn, show_alert=False)
    elif callback_data.model == 'off_channel':
        update_checkbox(is_true = False)
        print("off_channel")
        
        btn = channel_btn()
        # btn = channel_btn()
        await bot.edit_message_text(text="Kanallar", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=btn)
        # await call.answer(text="Kanallar", reply_markup=btn, show_alert=False)

async def status_all(call: CallbackQuery, bot: Bot, callback_data: AdminPanel):
    global user_views
    all_user = len(global_var)
    print(all_user)
    active_user = 0
    now = datetime.now()
    one_day_ago = (now - timedelta(hours=24)).isoformat()
    
    if global_var:
        for i in global_var:
            print(global_var[i])
            print(global_var[i])
            if global_var[i] > one_day_ago:
                active_user += 1
    print(active_user)

    movies = all_books()
    if movies:
        all_movies = len(movies)
    else:
        all_movies = 0
    
    active_movies = 0

    if user_views:
        for i in user_views:
            active_movies += len(user_views[i])
    
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    text = f"👥Umumiy foydalanuvchilar soni: <b>{all_user}</b>\n👤Aktiv foydalanuvchilar soni: <b>{active_user}</b>\n🎞Barcha Kitoblar soni: <b>{all_movies}</b>\n📥Jami yuklab olingan kitoblar: {active_movies}\n\n📅{date}"
    await bot.edit_message_text(text=text, chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=get_back_btn(model="admin_panel"))

# Sms xabar -------- start
async def send_answer_user(call: CallbackQuery, bot: Bot, callback_data: AdminPanel, state: FSMContext):
    await bot.edit_message_text(text="Xabar kiriting: ", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=get_back_btn(model="admin_panel"))
    await state.set_state(ForwardMessage.id)

async def answer_forward_id(message: types.Message, bot: Bot, state: FSMContext):
    global global_var
    global send_answer_messages
    global answer_users
    global sending_messages
    await state.update_data(id=message.text)
    send_answer_messages['chat_id'] = message.chat.id
    send_answer_messages['message_id'] = message.message_id
    send_answer_messages['reply_markup'] = message.reply_markup

    btn = adminpanel_btn(model='xabar_status')
    await bot.send_message(chat_id=message.from_user.id , text="Xabar yuborish boshlandi", reply_markup=btn)
    answer_users = global_var.copy()

    start = True
    
    for i in global_var.keys():
        if sending_messages:
            await bot.copy_message(chat_id=i, from_chat_id=send_answer_messages['chat_id'], message_id=send_answer_messages['message_id'], reply_markup=send_answer_messages['reply_markup'])
            
            del answer_users[i]
            await asyncio.sleep(3)
        else:
            start = False
            break
    
    if start:
        sending_users = len(global_var) - len(answer_users)
        no_sending_users = len(answer_users)
        date = datetime.now().strftime("%d-%m-%Y %H:%M")

        await message.answer(text=f"Xabar yuborish tugadi\n\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n\n📆{date}")
        answer_users = {}
        send_answer_messages = {}
        sending_messages = True
        await state.clear()
# Sms xabar -------- end

async def messages_status(call: CallbackQuery, bot: Bot):
    global sending_messages, global_var, answer_users, send_answer_messages

    total_users = len(global_var)
    sending_users = len(global_var) - len(answer_users)
    no_sending_users = len(answer_users)


    if sending_messages:
        text = f"Xabar yuborish\n\nYuborilmoqda: 👤Userlarga\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n👥Umumiy: {sending_users}/{total_users}\n\n📊Status: Davom etmoqda"
        await bot.edit_message_text(text=text, chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=status_message_btn(play="To'xtatish ⏸", model='stop', message_id=str(uuid.uuid4())))
    else:
        text = f"Yuborilmoqda: 👤Userlarga\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n👥Umumiy: {sending_users}/{total_users}\n\n📊Status: To'xtatilgan"
        await bot.edit_message_text(text=text, chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=status_message_btn(play="Davom etish ▶️", model='play', message_id=str(uuid.uuid4())))

async def pause_message(call: CallbackQuery, bot: Bot):
    global sending_messages
    global global_var
    global answer_users
    global send_answer_messages
    sending_messages = False

    total_users = len(global_var)
    sending_users = len(global_var) - len(answer_users)
    no_sending_users = len(answer_users)

    if sending_messages:
        text = f"Xabar yuborish\n\nYuborilmoqda: 👤Userlarga\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n👥Umumiy: {sending_users}/{total_users}\n\n📊Status: Davom etmoqda"
        btn = status_message_btn(play="To'xtatish ⏸", model='stop', message_id=str(uuid.uuid4()))
    else:
        text = f"Yuborilmoqda: 👤Userlarga\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n👥Umumiy: {sending_users}/{total_users}\n\n📊Status: To'xtatilgan"
        btn = status_message_btn(play="Davom etish ▶️", model='play', message_id=str(uuid.uuid4()))
    
    await bot.edit_message_text(text=text, chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=btn)

async def start_message(call: CallbackQuery, bot: Bot, state: FSMContext):
    global sending_messages
    global global_var
    global answer_users
    global send_answer_messages
    sending_messages = True

    total_users = len(global_var)
    sending_users = len(global_var) - len(answer_users)
    no_sending_users = len(answer_users)

    if sending_messages:
        text = f"Xabar yuborish\n\nYuborilmoqda: 👤Userlarga\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n👥Umumiy: {sending_users}/{total_users}\n\n📊Status: Davom etmoqda"
        btn = status_message_btn(play="To'xtatish ⏸", model='stop', message_id=str(uuid.uuid4()))
    else:
        text = f"Yuborilmoqda: 👤Userlarga\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n👥Umumiy: {sending_users}/{total_users}\n\n📊Status: To'xtatilgan"
        btn = status_message_btn(play="Davom etish ▶️", model='play', message_id=str(uuid.uuid4()))
    
    await bot.edit_message_text(text=text, chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=btn)
    await start_answer_users(call.message, bot, state)

async def start_answer_users(message: types.Message, bot: Bot, state: FSMContext):
    global send_answer_messages
    global sending_messages
    global global_var
    global answer_users
    
    users = answer_users.copy()
    start = True
    
    for i in users.keys():
        if sending_messages:
            await bot.copy_message(chat_id=i, from_chat_id=send_answer_messages['chat_id'], message_id=send_answer_messages["message_id"], reply_markup=send_answer_messages['reply_markup'])
            send_answer_messages['chat_id'] = message.chat.id
            send_answer_messages['message_id'] = message.message_id
            send_answer_messages['reply_markup'] = message.reply_markup
            del answer_users[i]
            await asyncio.sleep(3)
        else:
            start = False
            break
    
    if start:
        sending_users = len(global_var) - len(answer_users)
        no_sending_users = len(answer_users)
        date = datetime.now().strftime("%d-%m-%Y %H:%M")
        
        await message.answer(text=f"Xabar yuborish tugadi\n\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n\n📆{date}")
        answer_users = {}
        send_answer_messages = {}
        sending_messages = True
        await state.clear()

async def deleted_answers(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    global global_var, answer_users, send_answer_messages, sending_messages

    sending_users = len(global_var) - len(answer_users)
    no_sending_users = len(answer_users)
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    await call.message.answer(text=f"Xabar yuborish tugadi\n\n✅Yuborilgan: {sending_users}\n❌Yuborilmaganlar: {no_sending_users}\n\n📆{date}")
    answer_users = {}
    send_answer_messages = {}
    sending_messages = True
    await state.clear()


# all movies ------- start
async def books(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(text="Kitoblar ", chat_id=call.from_user.id, reply_markup=books_btn())

async def add_books(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text="Kitob nomini kiriting: ", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=get_back_btn(model="books"))
    await state.set_state(MoviesData.name)

async def delete_books(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text="Kitobni o'chirish uchun ustiga bir marta bosish kifoya: ", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=del_book_btn(data=all_books(), model="delete_book", go_back='books'))

async def del_books_id(call: CallbackQuery, bot: Bot, callback_data: DeleteChannel, state: FSMContext):
    delete_book_name_id(id=callback_data.id)
    await bot.edit_message_text(text="Kitobni o'chirish uchun ustiga bir marta bosish kifoya: ", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=del_book_btn(data=all_books(), model="delete_book", go_back='books'))
    await bot.send_message(chat_id=settings.bots.admin_id, text="Kitob o'chirildi!")
# all movies ------- end


# all Ads ------- start
async def add_ads(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(text="Reklama nomini kiriting: ", chat_id=call.from_user.id, reply_markup=get_back_btn('admin_panel'))

    await state.set_state(GetAds_data.name)

async def del_ads(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text="Reklamani o'chirish uchun ustiga bir marta bosish kifoya: ", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=del_book_btn(data=all_ads(), model="deleted_ads", go_back='admin_panel'))

async def del_ads_id(call: CallbackQuery, bot: Bot, callback_data: DeleteChannel, state: FSMContext):
    delete_ads(ads_id=callback_data.id)
    await bot.edit_message_text(text="Kitob o'chirish uchun ustiga bir marta bosish kifoya: ", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=del_book_btn(data=all_ads(), model="deleted_ads", go_back='admin_panel'))
    await bot.send_message(chat_id=settings.bots.admin_id, text="Reklama o'chirildi!")
# all Ads ------- end

async def add_saved(call: CallbackQuery, bot: Bot, callback_data: AddSaved):
    set_global_var(call.from_user.id, datetime.now().isoformat())

    book_id = callback_data.id
    user_id = callback_data.user_id

    movie = get_book_name_details(book_id=book_id)
    
    if insert_saved(book_id=book_id, users_id=user_id):
        btn = users_btn(data=movie, user_id=call.from_user.id)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=btn)

async def del_saved(call: CallbackQuery, bot: Bot, callback_data: DeleteSaved):
    set_global_var(call.from_user.id, datetime.now().isoformat())

    saved_id = callback_data.saved_id
    book_id = callback_data.movie_id
    
    book = get_book_name_details(movie_id=book_id)
    print(saved_id)

    delete_saved(saved_id=saved_id)
    btn = users_btn(data=book, user_id=call.from_user.id)
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=btn)

async def clear_admin(call: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


#  Next page
async def process_callback_next(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: SelectedBooks):
    page = callback_data.id
    data = search_book(callback_data.name)
    btn = search_books_btn(data=data, text=callback_data.name, page=page)
    await call.bot.answer_callback_query(call.id)
    await call.message.edit_text(text="Kitoblar ", reply_markup=btn)

async def process_callback_prev(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: SelectedBooks):
    page = callback_data.id
    data = search_book(callback_data.name)
    btn = search_books_btn(data=data, text=callback_data.name, page=page)
    await call.bot.answer_callback_query(call.id)
    await call.message.edit_text(text="Kitoblar ", reply_markup=btn)
