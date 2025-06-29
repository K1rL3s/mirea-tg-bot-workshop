import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token="8036313701:AAEp34lszpyd8eeLjDRUiEWjZA-6JO_Nxwg")
dp = Dispatcher()


@dp.message(F.text)
async def reply(message: Message) -> None:
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Лево верх"),
                KeyboardButton(text="Центр верх"),
                KeyboardButton(text="Право верх"),
            ],
            [
                KeyboardButton(text="Лево низ"),
                KeyboardButton(text="Центр низ"),
                KeyboardButton(text="Право низ"),
            ],
        ],
        resize_keyboard=True,
    )
    await message.answer(text=message.text, reply_markup=reply_keyboard)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
