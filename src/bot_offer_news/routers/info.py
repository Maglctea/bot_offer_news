from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

info_router = Router(name=__name__)


@info_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Здравствуйте. Напишите пожалуйста новость, которой хотите поделиться")
