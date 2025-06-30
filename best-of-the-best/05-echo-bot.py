import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message


bot = Bot(token="8036313701:AAEp34lszpyd8eeLjDRUiEWjZA-6JO_Nxwg")
dp = Dispatcher()


@dp.message()
async def echo(message: Message) -> None:
    await message.answer(text=message.text)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
