import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


bot = Bot(token="8036313701:AAEp34lszpyd8eeLjDRUiEWjZA-6JO_Nxwg")
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Привет!!!")


@dp.message(Command("help"))
async def help(message: Message) -> None:
    await message.answer("Ща помогу, ща, секунду")


@dp.message(F.text)
async def echo(message: Message) -> None:
    await message.answer(message.text)


@dp.message()
async def wtf(message: Message) -> None:
    await message.answer("Чего...")


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
