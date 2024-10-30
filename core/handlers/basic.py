from aiogram import Dispatcher, types, F, Bot
from aiogram.fsm.context import FSMContext

from core.keyboards.inline import adminpanel_btn, search_books_btn, get_back_btn, users_btn, sub_channel_keyboard
from aiogram.types import ReplyKeyboardRemove 
from core.states.states import GetChannel_data, MoviesData, GetAds_data
from core.db_api.db import (insert_channel, insert_books, insert_books_file,
                            search_book,insert_ads, update_book_view, get_book_name_details,
                            all_channels, get_checkbox,)
from core.config import set_global_var, global_var
# from core.filters.filter import check_subscription
from datetime import datetime, timedelta

from core.settings import settings

user_views = {}
answer_users = {}

# async def new_member(message: types.Message, bot: Bot):
#     # print(message.json())
#     new_members = f'{message.new_chat_member.user.first_name} {message.new_chat_member.user.last_name}'
#     print(new_members)
#     await bot.send_message(chat_id=message.chat.id, text=f"Xush kelibsiz, {new_members}!")

async def search_name_books(message: types.Message, bot: Bot):
    data = search_book(message.text)
    if data:
        btn = search_books_btn(data=data, text=message.text)
        await message.answer(text="Topildi:", reply_markup=btn)
    else:
        await message.reply(text="Bunday kitob topilmadi!")

async def admin_panel(message: types.Message, bot: Bot):
    print(message.from_user.id)
    print(settings.bots.admin_id)
    btn = adminpanel_btn(model='xabar')
    if int(message.from_user.id) == int(settings.bots.admin_id):
        await message.answer(text="Admin panel", reply_markup=btn)

# Channels ------ start
async def select_add_channel(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    btn = get_back_btn(model="channels")
    await bot.edit_message_text(text="Kanal nomini kiriting:", chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=btn)
    # await call.message.answer(text="Kanal nomini kiriting:", reply_markup=btn)
    await state.set_state(GetChannel_data.name)

async def answer_channel_name(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)
    btn = get_back_btn(model="channels")
    await message.answer(text="Kanal linkini kiriting:", reply_markup=btn)
    # await bot.edit_message_text(text="Kanal linkini kiriting:", chat_id=message.from_user.id, message_id=message.message_id, reply_markup=btn)
    await state.set_state(GetChannel_data.link)

async def answer_channel_link(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    print(data)
    
    answer = insert_channel(data['name'], data['link'])

    btn = get_back_btn(model="channels")
    if answer:
        await message.answer(text="Kanal qo'shildi!", reply_markup=btn)
    else:
        await message.answer(text="Bunday kanal oldindan mavjud!", reply_markup=btn)

    await state.clear()
# Channels ------ end

# Books --------- start
async def get_book_name(message: types.Message, bot: Bot, state: FSMContext):
    answer = insert_books(message.text)
    if answer:
        await state.update_data(name=message.text)
        btn = get_back_btn(model="books")
        await message.answer(text="Kitob qismini kiriting: ", reply_markup=btn)
        await state.set_state(MoviesData.part)
    else:
        await message.answer(text="Bunday kitob oldindan mavjud!\nIltimos boshqa nomdan foydalaning.", reply_markup=get_back_btn(model="books"))
        await state.set_state(MoviesData.name)


async def get_book_part(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(part=message.text)

    btn = get_back_btn(model="books")
    await message.answer(text="Kitob hajmini kiriting: ", reply_markup=btn)
    await state.set_state(MoviesData.size)

async def get_book_size(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(size=message.text)

    btn = get_back_btn(model="books")
    await message.answer(text="Kitob faylini yuboring:", reply_markup=btn)
    await state.set_state(MoviesData.file)

async def get_book_file(message: types.Message, bot: Bot, state: FSMContext):
    if message.document:
        file = message.document.file_id
        print("document file")
        print("document file")
        print("document file")

    elif message.audio:
        file = message.audio.file_id
        print("Audio file")
        print("Audio file")
        print("Audio file")

    data = await state.get_data()

    if file:
        if message.document:
            send_message = await bot.send_audio(chat_id=settings.bots.base_channel, audio=file, caption=f"Name: {data['name']}")
            file_id = send_message.document.file_id
            await state.update_data(video=file_id)
            file_data = search_book(data["name"])[0]
            answer_data = insert_books_file(name_id=file_data['id'], part=data['part'], size=data['size'], file=file_id, types='document')
        elif message.audio:
            send_message = await bot.send_video(chat_id=settings.bots.base_channel, video=file, caption=f"Name: {data['name']}")
            file_id = send_message.audio.file_id
            await state.update_data(video=file_id)
            file_data = search_book(data["name"])[0]
            answer_data = insert_books_file(name_id=file_data['id'], part=data['part'], size=data['size'], file=file_id, types='audio')

    btn = get_back_btn(model="books")
    if answer_data:
        await message.answer(text="Kitob qo'shildi!\nKeyingi kitob qismini kiriting:", reply_markup=btn)
    else:
        await message.answer(text="Bunday kitob oldindan mavjud!", reply_markup=btn)

    await state.set_state(MoviesData.part)
# Movie ---------- end

async def get_ads_name(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)
    btn = get_back_btn(model="admin_panel")
    await message.answer(text="Reklama linkini kiriting:", reply_markup=btn)
    await state.set_state(GetAds_data.link)

async def get_ads_link(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    print(data)
    
    answer = insert_ads(data['name'], data['link'])

    btn = get_back_btn(model="admin_panel")
    if answer:
        await message.answer(text="Reklama qo'shildi!", reply_markup=btn)
    else:
        await message.answer(text="Bunday reklama oldindan mavjud!", reply_markup=btn)

    await state.clear()

async def send_movies(message: types.Message, bot: Bot):
    global user_views
    if message.chat.type in ['group', 'supergroup', 'private']:
        text = (message.text).split(" ")
        await bot.send_message(chat_id=message.chat.id, text=f"Name: {text}")

        if text[1]:
            movie = get_book_name_details(book_id=int(text[1]))
        else:
            movie = get_book_name_details(book_id=int(text[1]))

        if movie:
            if message.chat.id not in user_views or message.chat.id in user_views and int(movie['id']) not in user_views[message.chat.id]:
                updates = update_book_view(id=movie['id'], view=int(movie['views'])+1)

            btn = users_btn(data=movie, user_id=message.chat.id)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.send_video(chat_id=message.chat.id, video=movie['video'], caption=f"{movie['name']}\n📀Hajmi: {movie['size']} MB\n👁: {movie['views']}\n👌@kino_bot", reply_markup=btn)
        else:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.send_message(chat_id=message.chat.id, text="Bu kodga mos kino topilmadi!")
    else:
        set_global_var(message.from_user.id, datetime.now().isoformat())

        text = (message.text).split(" ")
        if message.from_user.id not in user_views:
            user_views[message.from_user.id] = {}
        
        print()
        print(text)
        print()
        
        if text[1] != 'true':
            if text[1]:
                movie = get_book_name_details(movie_id=int(text[1]))
            else:
                movie = get_book_name_details(movie_id=int(text[1]))

            if movie:
                if message.from_user.id not in user_views or message.from_user.id in user_views and int(movie['id']) not in user_views[message.from_user.id]:
                    user_views[message.from_user.id][int(movie['id'])] = int(movie['id'])
                    updates = update_book_view(id=movie['id'], view=int(movie['views'])+1)

                btn = users_btn(data=movie, user_id=message.from_user.id)
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
                await bot.send_video(chat_id=message.from_user.id, video=movie['video'], caption=f"{movie['name']}\n📀Hajmi: {movie['size']} MB\n👁: {movie['views']}\n👌@kino_bot", reply_markup=btn)
            else:
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
                await bot.send_message(chat_id=message.from_user.id, text="Bu kodga mos kino topilmadi!")

async def send_movies_id(message: types.Message, bot: Bot):
    global user_views

    set_global_var(message.from_user.id, datetime.now().isoformat())

    text = message.text
    if message.from_user.id not in user_views:
        user_views[message.from_user.id] = {}

    
    movie = get_book_name_details(movie_id=int(text))

    if movie:
        if message.from_user.id not in user_views or message.from_user.id in user_views and int(movie['id']) not in user_views[message.from_user.id]:
            user_views[message.from_user.id][int(movie['id'])] = int(movie['id'])
            updates = update_book_view(id=movie['id'], view=int(movie['views'])+1)

        btn = users_btn(data=movie, user_id=message.from_user.id)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await bot.send_video(chat_id=message.from_user.id, video=movie['video'], caption=f"{movie['name']}\n📀Hajmi: {movie['size']} MB\n👁: {movie['views']}\n👌@kino_bot", reply_markup=btn)
    else:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await bot.send_message(chat_id=message.from_user.id, text="Bu kodga mos kino topilmadi!")

# async def searches_book(message: types.Message):
#     data = search_book(message.text)

#     if data:
#         btn = users_btn(data=data, user_id=message.from_user.id)
#         await message.answer(text="Kitob topildi!", reply_markup=btn)
#     else:
#         await message.answer(text="Kino topilmadi!")

async def sub_channel_answer(message: types.Message):
    await message.answer(f"Iltimos, kanalga obuna bo'ling va qayta urinib ko'ring.", parse_mode="HTML", reply_markup=sub_channel_keyboard())

async def sub_channel(call: types.CallbackQuery, bot: Bot):
    results = None
    user_id = call.from_user.id
    try:
        is_true = get_checkbox()
        if is_true['is_true']:
            channel_list = []
            channels = all_channels()
            
            if channels:
                for channel in channels:
                    links = str(channel['link']).replace('https://t.me/', '@')
                    member = await bot.get_chat_member(chat_id=links, user_id=user_id)
                    if member.status in ['member', 'administrator', "creator"]:
                        channel_list.append(True)
                    else:
                        channel_list.append(False)
            
            if False not in channel_list:
                results = True
            else:
                results = False
        else:
            results = True
    except Exception as e:
        print(e)
        results = None
    
    if results:
        text = f"🖐<b>Assalomu Alaykum,</b> <a href='tg://user?id={call.message.from_user.id}'>{call.message.from_user.full_name}</a>\n\nKitob topish uchun kitob nomini kiriting: "
        await call.message.answer(text=text)
    else:
        # btn = get_back_btn(model="admin_panel")
        await bot.answer_callback_query(call.id, text="Kanalga obuna bo'lmadingiz!", show_alert=False)


