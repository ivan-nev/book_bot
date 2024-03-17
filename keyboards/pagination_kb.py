from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


# Функция, генерирующая клавиатуру для страницы книги
def create_pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_buildel = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_buildel.row(*[
        InlineKeyboardButton(
            text=LEXICON.get(button, button), callback_data=button
        )
        for button in buttons
    ])
    # Возвращаем объект инлайн-клавиатуры
    return kb_buildel.as_markup()
