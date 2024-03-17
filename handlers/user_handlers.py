from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import users_db, user_dict_template
from filters.filters import IsDelBookmarkCallbckData, IsDigitalCallbckData
from keyboards.bookmarks_kb import create_bookmarks_kb, create_edit_bookmarks_kb
from keyboards.pagination_kb import create_pagination_kb
from lexicon.lexicon import LEXICON
from services.file_handling import book

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands='beginning'))
async def beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )

# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )

# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands='bookmarks'))
async def bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_kb(*users_db[message.from_user.id]['bookmarks'])
        )
    else:
        await message.answer(LEXICON['no_bookmarks'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == 'forward')
async def forward_callback(callback:CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    else:
        await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой

@router.callback_query(F.data == 'backward')
async def backward_callback(callback:CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -=1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'

            )
        )
    else:
        await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def add_bookmark(callback:CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(users_db[callback.from_user.id]['page'])
    await callback.answer(f'Страница {users_db[callback.from_user.id]["page"]} добавлена')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitalCallbckData())
async def procecc_bookmark_press(callback:CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == 'edit_bookmarks')
async def edit_bookmark(callback:CallbackQuery):
    text = LEXICON['edit_bookmarks']
    await callback.message.edit_text(
        text=text,
        reply_markup=create_edit_bookmarks_kb(*users_db[callback.from_user.id]['bookmarks'])
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbckData())
async def delete_bookmark(callback:CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['edit_bookmarks'],
            reply_markup=create_edit_bookmarks_kb(*users_db[callback.from_user.id]['bookmarks'])
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()

# Хандлер на кнопку Отмена
@router.callback_query(F.data == 'cancel')
async def cancel(callback:CallbackQuery):
    text = book[users_db[callback.from_user.id]['page']]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'

        )
    )
    await callback.answer()

