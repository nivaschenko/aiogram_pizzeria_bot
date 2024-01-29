from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import IsAdmin, ChatTypeFilter
from keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard(
    "Add Product",
    "Update Product",
    "Delete Product",
    "Just looking",
    placeholder="Make a choice",
    sizes=(2, 1, 1),
)


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Make a choice", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Just looking")
async def starring_at_product(message: types.Message):
    await message.answer("OK, Here is a list of products")


@admin_router.message(F.text == "Update Product")
async def change_product(message: types.Message):
    await message.answer("OK, Here is a list of products")


@admin_router.message(F.text == "Delete Product")
async def delete_product(message: types.Message):
    await message.answer("Select product(s) for deleting")


# Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Enter product name again:',
        'AddProduct:description': 'Enter description again:',
        'AddProduct:price': 'Enter price again:',
        'AddProduct:image': 'This step is last so...',
    }


@admin_router.message(StateFilter(None), F.text == "Add Product")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Add product name", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command("Cancel"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Canceled", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'), Command("Back"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "back")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer("You are on the first step. Print product name or print Cancel to exit")
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"You have returned to previous state \n{AddProduct.texts[previous.state]}")
        previous = step


@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.description)
    await message.answer("Add product description")


@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Product name should be a text. Please input a valid value")


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("Add product price")


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
    except ValueError as ex:
        await message.answer("The price could be integer only. Please enter correct value")
        return
    await state.update_data(price=price)
    await state.set_state(AddProduct.image)
    await message.answer("Загрузите изображение товара")


@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("The product has been added", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()
