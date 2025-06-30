import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import Database

bot = Bot(token="8036313701:AAEp34lszpyd8eeLjDRUiEWjZA-6JO_Nxwg")
dp = Dispatcher()
db = Database("database.db")


@dp.message(CommandStart())
async def start(message: Message) -> None:
    tg_id = message.from_user.id
    db.save_user(tg_id=tg_id)
    await message.answer("Привет! Я тебя запомнил =)")


@dp.message()
async def hello(message: Message) -> None:
    tg_id = message.from_user.id
    user = db.get_user(tg_id=tg_id)
    if user:
        text = "Привет, " + str(user.tg_id) + "!"
        await message.answer(text)
    else:
        await message.answer("Кажется, я тебя не знаю...")


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    try:
        dp.run_polling(bot)
    finally:
        db.close()


if __name__ == "__main__":
    main()
