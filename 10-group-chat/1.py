import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from database import Database


bot = Bot(token="8036313701:AAEp34lszpyd8eeLjDRUiEWjZA-6JO_Nxwg")
dp = Dispatcher()
db = Database("database.db")


@dp.message()
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
