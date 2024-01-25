from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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