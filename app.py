from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from core.settings import settings
# from core.keyboards.inline import client_user_btn
from core.handlers.basic import (admin_panel, select_add_channel, answer_channel_name, answer_channel_link,
                                 get_book_name, get_book_part, get_book_size, get_book_file, get_ads_link, get_ads_name,
                                 send_movies, send_movies_id, sub_channel_answer, sub_channel, search_name_books)
from core.handlers.callback import (deleted_answers, pause_message, process_callback_next, process_callback_prev, selected_channel, selected_admin_panel, selected_del_channel, deleted_channels,
                                     on_channels, books, add_books, start_answer_users, start_message, status_all, send_answer_user, answer_forward_id,
                                     delete_books, del_books_id, add_ads, del_ads, del_ads_id, 
                                     add_saved, del_saved, clear_admin, messages_status, selected_books_btn,
                                     selected_audio, selected_documents)
from core.utils.callbackdata import AdminPanel, DeleteChannel, AddSaved, DeleteSaved, SelectedBooks, Statistic
from core.states.states import GetChannel_data, ForwardMessage, MessageNext, MoviesData, GetAds_data
# from core.handlers.inlinemode import inline_echo
from core.config import set_global_var, global_var
from core.filters.filter import CheckSubChannel, CheckText, Checktext_two

from datetime import datetime, timedelta

import asyncio
import logging

async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Bot ishga tushdi!")
    # await bot.(chat_id="@searches_inline_bot", )


async def get_start(message: types.Message, bot: Bot):
    set_global_var(message.from_user.id, datetime.now().isoformat())
    print("test: ", global_var)
    text = f"🖐<b>Assalomu Alaykum,</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>\n\nKitob topish uchun kitob nomini kiriting: "
    
    await message.answer(text=text)


async def get_help(message: types.Message, bot: Bot):
    set_global_var(message.from_user.id, datetime.now().isoformat())
    text = f"🖐<b>Assalomu Alaykum,</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>\n\n"
    await message.answer(text=text)

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Bot to'xtadi!")


async def start():
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    logging.basicConfig(
        level="INFO",
        format="%(asctime)s - %(name)s - [ %(message)s ]",
        # format="%(asctime)s - ERROR - %(name)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S')
    
    dp = Dispatcher()
    dp.startup.register(start_bot)

    # dp.inline_query.register(inline_echo)
    dp.callback_query.register(selected_admin_panel, AdminPanel.filter(F.model =='admin_panel'))
    dp.callback_query.register(selected_channel, AdminPanel.filter(F.model =='channels'))
    dp.callback_query.register(select_add_channel, AdminPanel.filter(F.model =='add_channel'))
    dp.callback_query.register(selected_del_channel, AdminPanel.filter(F.model =='del_channel'))
    dp.callback_query.register(deleted_channels, DeleteChannel.filter(F.model =='delete_channel'))
    dp.callback_query.register(on_channels, AdminPanel.filter(F.model =='on_channel'))
    dp.callback_query.register(on_channels, AdminPanel.filter(F.model =='off_channel'))
    dp.callback_query.register(status_all, AdminPanel.filter(F.model =='statistic'))
    dp.callback_query.register(send_answer_user, AdminPanel.filter(F.model =='xabar'))
    dp.callback_query.register(sub_channel, AdminPanel.filter(F.model =='checksub') )
    dp.message.register(sub_channel_answer, CheckSubChannel())
    dp.message.register(answer_forward_id, ForwardMessage.id)
    # dp.chat_member.register(new_member)

    dp.callback_query.register(selected_books_btn, SelectedBooks.filter(F.model =='sel_bk'))
    dp.callback_query.register(selected_audio, SelectedBooks.filter(F.model =='audio'))
    dp.callback_query.register(selected_documents, SelectedBooks.filter(F.model =='document'))
    dp.callback_query.register(books, AdminPanel.filter(F.model =='books'))
    dp.callback_query.register(add_books, AdminPanel.filter(F.model =='add_book'))
    dp.callback_query.register(delete_books, AdminPanel.filter(F.model =='del_book'))
    dp.callback_query.register(del_books_id, DeleteChannel.filter(F.model =='delete_book'))
    dp.callback_query.register(add_ads, AdminPanel.filter(F.model =='add_ads'))
    dp.callback_query.register(del_ads, AdminPanel.filter(F.model =='del_ads'))
    dp.callback_query.register(del_ads_id, DeleteChannel.filter(F.model =='deleted_ads'))
    dp.callback_query.register(add_saved, AddSaved.filter(F.model =='add_save'))
    dp.callback_query.register(del_saved, DeleteSaved.filter(F.model =='del_save'))
    dp.callback_query.register(clear_admin, AdminPanel.filter(F.model =='clear'))
    dp.callback_query.register(messages_status, AdminPanel.filter(F.model =='xabar_status'))
    dp.callback_query.register(messages_status, AdminPanel.filter(F.model =='update'))
    dp.callback_query.register(pause_message, Statistic.filter(F.model =='stop'))
    dp.callback_query.register(start_message, Statistic.filter(F.model =='play'))
    dp.callback_query.register(deleted_answers, AdminPanel.filter(F.model =='delete_status'))
    # dp.message.register(start_answer_users, MessageNext.model)
    dp.message.register(get_ads_name, GetAds_data.name)
    dp.message.register(get_ads_link, GetAds_data.link)
    dp.message.register(get_book_name, MoviesData.name)
    dp.message.register(get_book_part, MoviesData.part)
    dp.message.register(get_book_size, MoviesData.size)
    dp.message.register(get_book_file, MoviesData.file)
    dp.message.register(answer_channel_name, GetChannel_data.name)
    dp.message.register(answer_channel_link, GetChannel_data.link)
    # dp.message.register(send_movies, Checktext_two())
    # dp.message.register(send_movies_id, CheckText())
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_help, Command(commands='help'))
    dp.message.register(admin_panel, Command(commands='admin'))
    dp.message.register(search_name_books, F.text)
    dp.callback_query.register(process_callback_next, SelectedBooks.filter(F.model =='next'))
    dp.callback_query.register(process_callback_prev, SelectedBooks.filter(F.model =='prev'))

    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())