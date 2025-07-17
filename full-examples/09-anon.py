import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import Database


bot = Bot(token="7779550029:AAG0c9MlTcZBIo1ltdEqdmS0xnwkZZQ_xmU")
dp = Dispatcher()
db = Database("database.db")


class AnonSG(StatesGroup):
    message = State()


# https://t.me/botusername?start=123123
@dp.message(
    CommandStart(deep_link=True),
    MagicData(F.command.args.isdigit()),
    MagicData(F.command.args.cast(int).as_("receiver_id")),
)
async def deeplink_start(message: Message, receiver_id: int, state: FSMContext) -> None:
    # Сохраняем юзера-отправителя в базу
    db.save_user(message.from_user.id)

    # Ищем юзера-получателя
    receiver = db.get_user_by_id(receiver_id)
    if receiver:
        # Если получатель существует, ставим состояние и ждём сообщение
        await state.set_state(AnonSG.message)
        await state.set_data({"receiver_id": receiver_id})
        await message.answer("Жду от тебя тайное сообщение")
    else:
        # Иначе пишем что анлак
        await message.answer("Не нашёл такого пользователя, попроси ссылку ещё раз")


@dp.message(CommandStart())
async def default_start(message: Message) -> None:
    # Сохраняем юзера-отправителя в базу
    db.save_user(message.from_user.id)

    # Отправляем юзеру его ссылку для анонимок
    user = db.get_user_by_tg_id(message.from_user.id)
    bot_info = await bot.me()
    text = f"Привет! Твоя ссылка: t.me/{bot_info.username}?start={user.id}"
    await message.answer(text=text)


@dp.message(AnonSG.message)
async def anon_message(message: Message, state: FSMContext) -> None:
    # Берём юзера-получателя из базы
    data = await state.get_data()
    receiver_id: int = data["receiver_id"]
    receiver = db.get_user_by_id(receiver_id)

    # Берём юзера-отправителя из базы
    sender = db.get_user_by_tg_id(message.from_user.id)

    # Делаем Inline клавиатуру, чтобы получатель мог отправить ответ отправителю
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Написать в ответ", callback_data=str(sender.id))
        ]]
    )

    # Отправляем получателю тайное сообщение
    title_message = await bot.send_message(
        chat_id=receiver.tg_id,
        text="У тебя новое сообщение!",
        reply_markup=keyboard,
    )
    await message.send_copy(
        chat_id=receiver.tg_id,
        reply_to_message_id=title_message.message_id,
    )

    # Пишем отправителю, что всё ок
    await message.reply("Передал сообщение ;)\nМожешь передать что-нибудь ещё")

    # Состояние не чистим, отправитель может написать ещё что-то получателю


@dp.callback_query()
async def deeplink_callback(callback: CallbackQuery, state: FSMContext) -> None:
    # Берём айди юзера-получателя из кнопки, тк мы его туда положили
    receiver_id = int(callback.data)

    # Ставим состояние и ждём сообщение.
    # Не проверяем, что отправитель есть, тк из кнопки он точно будет
    await state.set_state(AnonSG.message)
    await state.set_data({"receiver_id": receiver_id})
    await callback.message.reply("Жду от тебя тайное сообщение")


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    try:
        dp.run_polling(bot)
    finally:
        db.close()


if __name__ == "__main__":
    main()
