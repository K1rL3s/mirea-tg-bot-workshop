import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database import Database


bot = Bot(token="8036313701:AAEp34lszpyd8eeLjDRUiEWjZA-6JO_Nxwg")
dp = Dispatcher()
db = Database("database.db")


class DirectMessage(StatesGroup):
    wait_message = State()


@dp.callback_query()
async def wait_dm_message(callback: CallbackQuery, state: FSMContext) -> None:
    receiver_id = int(callback.data)
    receiver = db.get_user_by_id(receiver_id)

    await state.set_state(DirectMessage.wait_message)
    await state.set_data(data={"receiver_id": receiver_id})

    text = "Напиши сообщение, которое отправится " + receiver[2]
    await callback.message.answer(text)


@dp.message(DirectMessage.wait_message)
async def dm_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    receiver_id: int = data["receiver_id"]
    receiver = db.get_user_by_id(receiver_id)

    sender = db.get_user_by_tg_id(tg_id=message.from_user.id)

    title_text = "Сообщение от " + sender.name + " лично для тебя:"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ответ в лс", callback_data=str(sender.id))]
        ]
    )
    title_message = await bot.send_message(chat_id=receiver.tg_id, text=title_text, reply_markup=keyboard)
    await message.send_copy(chat_id=receiver.tg_id, reply_to_message_id=title_message.message_id)

    await message.answer("Личное сообщение отправлено!")


@dp.message()
async def group_message(message: Message) -> None:
    sender = db.get_user_by_tg_id(message.from_user.id)
    if not sender:
        return

    users = db.get_all_users()
    title_text = "Сообщение от " + sender.name + " для всех:"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ответ в лс", callback_data=str(sender.id))]
        ]
    )
    for receiver in users:
        if receiver == sender:
            continue
        title_message = await bot.send_message(chat_id=receiver.tg_id, text=title_text, reply_markup=keyboard)
        await message.send_copy(chat_id=receiver.tg_id, reply_to_message_id=title_message.message_id)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    try:
        dp.run_polling(bot)
    finally:
        db.close()


if __name__ == "__main__":
    main()