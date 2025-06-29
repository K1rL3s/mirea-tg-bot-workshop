from aiogram import F, Dispatcher
from aiogram.filters import Command, CommandStart

dp = Dispatcher()

@dp.message(F.text == "/start")
async def first() -> ...:
    ...

@dp.message(Command("start"))
async def second() -> ...:
    ...

@dp.message(CommandStart())
async def third() -> ...:
    ...
