import time
from string import punctuation

from aiogram import types, Router, Bot, F
from aiogram.filters import or_f, Command

from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'pig', 'lion', 'lizard'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_router.message(
    or_f(Command('admin'), F.text.lower() == 'admin')
)
async def get_adminis(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list

    if message.from_user.id in admins_list:
        await message.answer('Admins list have been updated')
    else:
        await message.answer('You are not in admin list')

    await message.delete()



@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(
            f"{message.from_user.first_name}, be friendly in the chat"
        )
        await message.delete()
