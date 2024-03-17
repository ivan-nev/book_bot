from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

#проверяет callback_data у объекта CallbackQuery на то, что он состоит из цифр
class IsDigitalCallbckData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


# фильтр будет ловить callback_data от кнопок-закладок, которые нужно удалить в режиме редактирования закладок.
class IsDelBookmarkCallbckData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()