from aiogram import types, Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from filters.chat_types import ChatTypeFilter
from filters.message_types import MessageContentTypeFilter
from keyboards.reply import start_kb3

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        text='Hi, I\'m personal assistant',
        reply_markup=start_kb3.as_markup(
            resize_keyboard=True,
            input_field_placeholder='Select an option'
        )
    )


@user_private_router.message(
    or_f(Command('navigation'), (F.text.lower() == 'navigation'))
)
async def menu_cmd(message: types.Message):
    await message.answer(message.text)


@user_private_router.message(
    or_f(Command('about'), (F.text.lower() == 'about'))
)
async def about_cmd(message: types.Message):
    await message.answer('About our company')


@user_private_router.message(
    or_f(Command('payment'), (F.text.lower() == 'payment'))
)
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Payment options:"),
        "Online",
        "Upon receipt",
        "At the establishment",
        marker='✅ '
    )
    await message.answer(text.as_html())


@user_private_router.message(
    (F.text.lower() == 'shipping method') |
    F.text.lower().contains('ship')
)
@user_private_router.message(Command('shipping'))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Shipping options:"),
            "Courier",
            "Pickup",
            "At the establishment",
            marker='✅ '
        ),
        as_marked_section(
            Bold("Not supporting:"),
            "Post",
            "Birds",
            marker='❌ '
        ),
        sep='\n-----------------------\n'
    )
    await message.answer(
        text.as_html()
    )


@user_private_router.message(
    (F.text.lower() == 'Request contact') |
    F.text.lower().contains('Request contact')
)
@user_private_router.message(Command('reviews'))
async def review_cmd(message: types.Message):
    await message.answer(
        text="reviews"
    )


@user_private_router.message(MessageContentTypeFilter([ContentType.CONTACT]))
async def receive_contact(message: types.Message):
    contact = message.contact
    await message.answer(
        f"<b>Thanks, {contact.first_name}!</b> "
        f"Your phone number is {contact.phone_number}"
    )


@user_private_router.message(F.location)
async def receive_contact(message: types.Message):
    location = message.location
    await message.answer(
        f"Thanks! "
        f"Your location is {location}"
    )
