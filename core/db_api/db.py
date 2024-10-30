import sqlite3

# Ma'lumotlar bazasini yaratish yoki unga ulanish
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Kino jadvali
c.execute('''
    CREATE TABLE IF NOT EXISTS book_name (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        views INT NOT NULL DEFAULT 0,
        name TEXT NOT NULL
    )''')

c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_id INT,
        part TEXT NOT NULL,
        size REAL NOT NULL,
        file TEXT NOT NULL,
        types TEXT NOT NULL,
        FOREIGN KEY(name_id) REFERENCES book_name(id) ON DELETE CASCADE
    )''')

c.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        link TEXT NOT NULL,
        is_true Boolen NOT NULL DEFAULT False
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        link TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS saveds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        users_id INT NOT NULL,
        book_id INT,
        FOREIGN KEY(book_id) REFERENCES book_name(id) ON DELETE CASCADE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS is_trues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        checkbox Boolen NOT NULL default False
    )
''')

c.execute('''SELECT * FROM is_trues''')

checks = c.fetchone()

# print(checks)
if checks is None:
    c.execute('''
            INSERT INTO is_trues (checkbox) VALUES (?)
        ''', (False,))

conn.commit()
conn.close()

def insert_books(name):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT name FROM book_name WHERE name=?
    ''', (name,))
    
    movie = c.fetchone()
    if movie is None:
        c.execute('''
            INSERT INTO book_name (name) VALUES (?)
        ''', (name,))

        is_true = True
    else:
        is_true = False
    
    conn.commit()
    conn.close()

    return is_true

def insert_books_file(name_id, part, size, file, types):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    
    movie = c.fetchone();
    if movie is None:
        c.execute('''
            INSERT INTO books (name_id, part, size, file, types) VALUES (?, ?, ?, ?, ?)
        ''', (name_id, part, float(size), file, types))

        is_true = True
    else:
        is_true = False
    
    conn.commit()
    conn.close()

    return is_true

# Misol uchun ma'lumot kiritish
# print(insert_movie('Film nomi', 700.2, '789456'))

# SELECT saveds.id, saveds.book_id, saveds.users_id, book_name.name, book_name.views FROM saveds JOIN
            #    book_name ON book_name.id = saveds.book_id WHERE saveds.users_id = ?
    # ''', (users_id,))

def get_book_name_details(book_id, types):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT books.id, books.name_id, books.part, books.size, books.file, books.types, book_name.name, book_name.id FROM books 
                JOIN book_name ON book_name.id = books.name_id WHERE name_id=? and types=?
    ''', (book_id, types))

    books = c.fetchall()
    conn.close()

    if books:
        resault = []
        for book in books:
            resault.append({'id': book[0], 'name_id': book[1], 'part': book[2], 'size': book[3], 'file': book[4], 'types': book[5], 'name': book[6]})
        return resault
    else:
        return None

# Misol uchun detalni olish
# movie_details = get_movie_details(1)


# Qidirish funksiyasi
def search_book(book_name):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT id, name, views FROM book_name WHERE name LIKE ?
    ''', ('%' + book_name + '%',))

    movies = c.fetchall()
    conn.close()

    if movies:
        result = []
        for movie in movies:
            result.append({'id': movie[0], 'name': movie[1], 'views': movie[2]})
        return result
    else:
        return None

# Misol uchun qidirish
# movies_found = search_movie('i')
# print(search_movie('i'))
def update_book_view(id, view):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    # Qaysi ustunlarni yangilash kerakligini aniqlash
    if view:
        c.execute(f"UPDATE book_name SET views = {view} WHERE id = {id}")

    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    
    if rows_affected > 0:
        print(f"ID: {id} bo'yicha save ma'lumotlari yangilandi.")
        return True
    else:
        print(f"ID: {id} bo'yicha save topilmadi yoki yangilanmadi.")
        return False

# print(update_movies(id=1, view=1))

def all_books():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT * FROM book_name
    ''')

    movies = c.fetchall()
    conn.close()

    if movies:
        result = []
        for movie in movies:
            result.append({'id': movie[0], 'name': movie[2], 'views': movie[1]})
        return result
    else:
        return None

# print(all_movie())
# movies_found = all_movie()
def delete_book_name_id(id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        DELETE FROM book_name WHERE id=?
    ''', (id,))

    conn.commit()
    conn.close()

def delete_books_id(id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        DELETE FROM books WHERE id=?
    ''', (id,))

    conn.commit()
    conn.close()


# Kanal uchun ---
def insert_channel(name, link, is_true=False):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT name, link FROM channels WHERE name=? and link=?
    ''', (name, link))
    
    channel = c.fetchone()
    if channel is None:
        c.execute('''
            INSERT INTO channels (name, link, is_true) VALUES (?, ?, ?)
        ''', (name, link, is_true))

        check = True
    else:
        check = False
    
    conn.commit()
    conn.close()

    return check


# print(insert_channel('Channel', 'channel', False))
# Kanalga murojat qilib olish
def get_channel_details(channel_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT name, link, is_true FROM channels WHERE id=?
    ''', (channel_id,))

    channel = c.fetchone()
    conn.close()

    if channel:
        return {'name': channel[0], 'size': channel[1], 'is_true': channel[2]}
    else:
        return None

# a = get_channel_details(1)
# print(a)
def all_channels():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT * FROM channels
    ''')

    channels = c.fetchall()
    conn.close()

    if channels:
        result = []
        for channel in channels:
            result.append({'id': channel[0], 'name': channel[1], 'link': channel[2], 'is_true': channel[3]})
        return result
    else:
        return None

# Kanal o'chirish
def delete_channel(channel_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        DELETE FROM channels WHERE id=?
    ''', (channel_id,))

    conn.commit()
    conn.close()
    print(f"ID: {channel_id} bo'yicha kanal o'chirildi.")

# Kanal o'zgartirish
def update_channel_details(channel_id, is_true=None):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    # Qaysi ustunlarni yangilash kerakligini aniqlash
    if is_true is not None:
        c.execute(f"UPDATE channels SET is_true = ? WHERE id = ?", (is_true, channel_id))

    rows_affected = c.rowcount
    conn.close()
    
    if rows_affected > 0:
        print(f"ID: {channel_id} bo'yicha kanal ma'lumotlari yangilandi.")
        return True
    else:
        print(f"ID: {channel_id} bo'yicha kanal topilmadi yoki yangilanmadi.")
        return False

# Misol uchun yangilash
# channel_id = 2
# result = update_channel_details(channel_id, is_true=True)
# print(f"Yangilash muvaffaqiyatli bo'ldimi? {result}")

# Reklama uchun
def insert_ads(name, link):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT name, link FROM ads WHERE name=?
    ''', (name,))
    
    ads = c.fetchone()
    if ads is None:
        c.execute('''
            INSERT INTO ads (name, link) VALUES (?, ?)
        ''', (name, link))

        check = True
    else:
        check = False
    
    conn.commit()
    conn.close()

    return check
# print(insert_ads('Reklama', 'reklama'))

# Reklamaga murojat qilib olish
def get_ads_details(ads_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT id, name, link FROM ads WHERE id=?
    ''', (ads_id,))

    ads = c.fetchone()
    conn.close()

    if ads:
        return {'id': ads[0], 'name': ads[1], 'link': ads[2]}
    else:
        return None
# print(get_ads_details(1))

def all_ads():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT * FROM ads
    ''')

    ads = c.fetchall()
    conn.close()

    if ads:
        result = []
        for ad in ads:
            result.append({'id': ad[0], 'name': ad[1], 'link': ad[2]})
        return result
    else:
        return None

# Reklama o'chirish
def delete_ads(ads_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        DELETE FROM ads WHERE id=?
    ''', (ads_id,))

    conn.commit()
    conn.close()
    print(f"ID: {ads_id} bo'yicha kanal o'chirildi.")
# delete_ads(1)

# Saved uchun
def insert_saved(book_id, users_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT book_id, users_id FROM saveds WHERE users_id=? and book_id=?
    ''', (users_id, book_id))
    
    saved = c.fetchone()
    if saved is None:
        c.execute('''
            INSERT INTO saveds (book_id, users_id) VALUES (?, ?)
        ''', (book_id, int(users_id)))

        check = True
    else:
        check = False
    
    conn.commit()
    conn.close()

    return check
# print(insert_saved(movie_id=1, users_id=4571))

# saved user_id ga teng bolganlarga murojat qilish
def get_saveds(users_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT saveds.id, saveds.book_id, saveds.users_id, book_name.name, book_name.views FROM saveds JOIN
               book_name ON book_name.id = saveds.book_id WHERE saveds.users_id = ?
    ''', (users_id,))

    saveds = c.fetchall()
    conn.close()
    results = []
    
    if saveds:
        for saved in saveds:
            results.append({'id':saved[0], 'book_id': saved[1], 'users_id': saved[2], 'name': saved[3], 'views': saved[4]})

    if results:
        return results
    else:
        return None
# print(get_saveds(4571))

def get_saveds_books_id(users_id, book_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT saveds.id, saveds.book_id, saveds.users_id, book_name.name, book_name.views FROM saveds JOIN
               book_name ON book_name.id = saveds.book_id WHERE saveds.users_id = ? AND saveds.book_id = ?
    ''', (users_id, book_id))

    saved = c.fetchone()
    conn.close()

    if saved:
        return {'id':saved[0], 'book_id': saved[1], 'users_id': saved[2], 'name': saved[3], 'views': saved[4]}
    else:
        return None

def delete_saved(saved_id):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        DELETE FROM saveds WHERE id=?
    ''', (saved_id,))

    conn.commit()
    conn.close()
    print(f"ID: {saved_id} bo'yicha saqlangan kino o'chirildi.")

def get_checkbox():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('''
        SELECT id, checkbox FROM is_trues WHERE id=?
    ''', (1,))

    check_true = c.fetchone()
    conn.close()

    if check_true:
        return {'id': check_true[0], 'is_true': check_true[1]}
    else:
        return None

def update_checkbox(is_true):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    # Qaysi ustunlarni yangilash kerakligini aniqlash
    if is_true is not None:
        c.execute(f"UPDATE is_trues SET checkbox = ? WHERE id = ?", (is_true, 1))

    conn.commit()
    conn.close()



# update_checkbox(is_true = False)
# print(get_checkbox())

