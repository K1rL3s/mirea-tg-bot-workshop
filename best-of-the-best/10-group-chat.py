import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database_10 import Database


bot = Bot(token="8036313701:AAEp34lszpyd8eeLjDRUiEWjZA-6JO_Nxwg")
dp = Dispatcher()
db = Database("database.db")


class Form(StatesGroup):
    name = State()
    age = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id

    user = db.get_user(tg_id=tg_id)
    if user:
        user_str = str(user.tg_id) + " " + user.name + " " + str(user.age)
        text = "Я тебя знаю, ты " + user_str
        await message.answer(text=text)
    else:
        await message.answer("Привет! Давай знакомиться. Напиши, как тебя зовут")
        await state.set_state(Form.name)


@dp.message(F.text, Form.name)
async def name_form(message: Message, state: FSMContext) -> None:
    name = message.text.strip()[:30]
    await state.update_data(name=name)

    await message.answer("Теперь введи, сколько тебе лет, " + name)

    await state.set_state(Form.age)


@dp.message(F.text.isdigit(), F.text.cast(int).as_("age"), Form.age)
async def age_form(message: Message, state: FSMContext, age: int) -> None:
    data = await state.get_data()
    name: str = data["name"]
    tg_id = message.from_user.id

    db.save_user(tg_id=tg_id, name=name, age=age)

    text = "Супер! Теперь ты " + str(tg_id) + " " + name + " " + str(age)
    await message.answer(text=text)

    await state.clear()


@dp.message(StateFilter(None))
async def group_message(message: Message) -> None:
    sender = db.get_user(message.from_user.id)
    if not sender:
        return

    users = db.get_all_users()
    title_text = "Сообщение от " + sender.name + " для всех:"

    for receiver in users:
        title_message = await bot.send_message(chat_id=receiver.tg_id, text=title_text)
        await message.send_copy(chat_id=receiver.tg_id, reply_to_message_id=title_message.message_id)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    try:
        dp.run_polling(bot)
    finally:
        db.close()


if __name__ == "__main__":
    main()
