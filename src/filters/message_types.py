from aiogram.enums import ContentType
from aiogram.filters import Filter
from aiogram import types


class MessageContentTypeFilter(Filter):
    def __init__(self, message_types: list[ContentType]):
        self.message_types = message_types

    async def __call__(self, message: types.Message) -> bool:
        return message.content_type in self.message_types
