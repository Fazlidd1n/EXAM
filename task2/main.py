import asyncio, logging, sys, requests
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import Dispatcher, Bot, filters
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from bs4 import BeautifulSoup

BOT_TOKEN = "6334253807:AAHuBzG7B-hIlQw41Fw2TTYHiWaQ1XxF6lY"
dp = Dispatcher(storage=MemoryStorage())


class States(StatesGroup):
    menu = State()
    start_menu = State()
    woman = State()
    men = State()
    last_menu = State()


def menu_buttons():
    btn1 = KeyboardButton(text="Fillial 📍")
    btn2 = KeyboardButton(text="Start ✅")
    btn3 = KeyboardButton(text="Admin 👨🏻‍💻")
    return ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3]], resize_keyboard=True, one_time_keyboard=True)


def start_menu():
    btn1 = KeyboardButton(text="Woman")
    btn2 = KeyboardButton(text="Men")
    btn3 = KeyboardButton(text="🔙 back")
    return ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3]], resize_keyboard=True, one_time_keyboard=True)


def woman_menu():
    btn1 = KeyboardButton(text="1-oy")
    btn2 = KeyboardButton(text="2-oy")
    btn3 = KeyboardButton(text="3-oy")
    btn4 = KeyboardButton(text="4-oy")
    btn5 = KeyboardButton(text="🔙 back")
    return ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3, btn4], [btn5]], resize_keyboard=True,
                               one_time_keyboard=True)


def men_menu():
    btn1 = KeyboardButton(text="1-oy")
    btn2 = KeyboardButton(text="2-oy")
    btn3 = KeyboardButton(text="3-oy")
    btn4 = KeyboardButton(text="4-oy")
    btn5 = KeyboardButton(text="🔙 back")
    return ReplyKeyboardMarkup(keyboard=[[btn1, btn2], [btn3, btn4], [btn5]], resize_keyboard=True,
                               one_time_keyboard=True)


def last_menu():
    btn1 = KeyboardButton(text="Dushanba")
    btn2 = KeyboardButton(text="Seshanba")
    btn3 = KeyboardButton(text="Chorshanba")
    btn4 = KeyboardButton(text="Payshanba")
    btn5 = KeyboardButton(text="Juma")
    btn6 = KeyboardButton(text="Shanba")
    btn7 = KeyboardButton(text="🔙 back")
    return ReplyKeyboardMarkup(keyboard=[[btn1, btn2, btn3], [btn4, btn5, btn6], [btn7]], resize_keyboard=True,
                               one_time_keyboard=True)


@dp.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer(f"Hello - 👤 {msg.from_user.full_name}", reply_markup=menu_buttons())
    print(f"👤 - {msg.from_user.full_name}")
    await state.set_state(States.menu)


@dp.message(States.menu)
async def menu_handler(msg: Message, state: FSMContext):
    if msg.text == "Fillial 📍":
        await msg.answer("Locatsiya 😂", reply_markup=menu_buttons())
    elif msg.text == "Start ✅":
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=start_menu())
        await state.set_state(States.start_menu)
    elif msg.text == "Admin 👨🏻‍💻":
        await msg.answer("@f_ismoilovv", reply_markup=menu_buttons())


@dp.message(States.start_menu)
async def start_handler(msg: Message, state: FSMContext):
    if msg.text == "Woman":
        await state.set_state(States.woman)
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=woman_menu())

    elif msg.text == "Men":
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=men_menu())
        await state.set_state(States.men)

    elif msg.text == "🔙 back":
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=menu_buttons())
        await state.set_state(States.menu)


@dp.message(States.woman)
async def woman_handler(msg: Message, state: FSMContext):
    if msg.text in ["1-oy", "2-oy", "3-oy", "4-oy"]:
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=last_menu())
        await state.set_state(States.last_menu)

    elif msg.text == "🔙 back":
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=start_menu())
        await state.set_state(States.start_menu)


@dp.message(States.men)
async def men_handler(msg: Message, state: FSMContext):
    if msg.text in ["1-oy", "2-oy", "3-oy", "4-oy"]:
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=last_menu())
        await state.set_state(States.last_menu)

    elif msg.text == "🔙 back":
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=start_menu())
        await state.set_state(States.start_menu)


@dp.message(States.last_menu)
async def last_handler(msg: Message, state: FSMContext):
    if msg.text in ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba"]:
        await msg.answer("Tugadi ❗️", reply_markup=last_menu())
        await state.set_state(States.last_menu)
    elif msg.text == "🔙 back":
        await msg.answer("Quyidagilarni birini tanlang ⤵️", reply_markup=men_menu())
        await state.set_state(States.men)


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
