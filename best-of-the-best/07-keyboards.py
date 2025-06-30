import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

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


@dp.message()
async def inline(message: Message) -> None:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Лево верх", callback_data="left_up"),
                InlineKeyboardButton(text="Центр верх", callback_data="center_up"),
                InlineKeyboardButton(text="Право верх", callback_data="right_up"),
            ],
            [
                InlineKeyboardButton(text="Лево низ", callback_data="left_down"),
                InlineKeyboardButton(text="Центр низ", callback_data="center_down"),
                InlineKeyboardButton(text="Право низ", callback_data="right_down"),
            ],
        ],
    )
    await message.answer(text=message.text, reply_markup=inline_keyboard)


@dp.callback_query()
async def callback_handler(callback: CallbackQuery) -> None:
    await callback.answer(text=callback.data, show_alert=True)
    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[]),
    )


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
