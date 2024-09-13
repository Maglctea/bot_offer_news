from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, MenuButtonWebApp, WebAppInfo, KeyboardButton

import settings

router = Router(name=__name__)


@router.message(Command("settings"))
async def cmd_settings(message: Message, bot: Bot):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Добавить бота', web_app=WebAppInfo(url=f'{settings.API_URL}/api/static/add_bot_form.html')),
             ],
            [
                KeyboardButton(text='Удалить бота', web_app=WebAppInfo(url=f'{settings.API_URL}/api/static/delete_bot_form.html'))
            ]

        ]
    )
    await message.answer(text='Здравствуйте. Выберите желаемое действие', reply_markup=markup)
