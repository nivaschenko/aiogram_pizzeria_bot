from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contacts: int = None,
        request_location: int = None,
        sizes: tuple = (2,),
) -> ReplyKeyboardMarkup:
    """
    Parameters request_contacts and request_location must be as indexes of btns args for buttons you need
    :param btns:
    :param placeholder:
    :param request_contacts:
    :param request_location:
    :param sizes:
    :return ReplyKeyboardBuilder:
    """

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contacts and request_contacts == index:
            keyboard.add(KeyboardButton(text=text, request_contacts=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder
    )






start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Navigation'),
            KeyboardButton(text='About'),
        ],
        [
            KeyboardButton(text='Shipping options'),
            KeyboardButton(text='Payment')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Select an option'
)

del_kb = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='Navigation'),
    KeyboardButton(text='About'),
    KeyboardButton(text='Shipping options'),
    KeyboardButton(text='Payment')
)
start_kb2.adjust(2,2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(
    text='Request contact', request_contact=True)
)

start_kb3.add(KeyboardButton(
    text='Request location', request_location=True)
)

start_kb3.row(
    KeyboardButton(
        text='Questionnaire', request_poll=KeyboardButtonPollType()
    )
)

start_kb3.adjust(2,2)