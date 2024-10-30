from aiogram.filters.callback_data import CallbackData

class AdminPanel(CallbackData, prefix="admin"):
    model: str

class Statistic(AdminPanel, prefix="statistic"):
    model: str
    id: str

class DeleteChannel(AdminPanel, prefix="delete_channel"):
    model: str
    id: int

class SelectedBooks(AdminPanel, prefix="select_books"):
    model: str
    name: str
    id: int

class AddSaved(AdminPanel, prefix="add_saved"):
    model: str
    user_id: str
    id: int

class DeleteSaved(AdminPanel, prefix="delete_saved"):
    model: str
    saved_id: int
    movie_id: int