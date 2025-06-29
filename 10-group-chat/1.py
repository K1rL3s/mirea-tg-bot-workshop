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
    title_text = "Сообщение от " + str(sender[1]) + " для всех:"

    for user in users:
        title_message = await bot.send_message(chat_id=user[0], text=title_text)
        await message.send_copy(chat_id=user[0], reply_to_message_id=title_message.id)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    try:
        dp.run_polling(bot)
    finally:
        db.close()


if __name__ == "__main__":
    main()
