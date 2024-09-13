import logging

from aiogram import Router, Bot
from aiogram.enums import ChatType
from aiogram.types import Message
from dishka import FromDishka

from bot_offer_news.db.gate.bot import BotGateway
from bot_offer_news.dto.bot import BotDTO
from bot_offer_news.filters.chat_type import ChatTypeFilter
from bot_offer_news.services.bot import send_message

logger = logging.getLogger(__name__)

news_router = Router(name=__name__)


@news_router.message(ChatTypeFilter(chat_type=[ChatType.PRIVATE]))
async def message_handler(message: Message, bot: Bot, bot_gate: FromDishka[BotGateway]) -> None:
    if message.from_user.is_bot:
        return
    bot_info: BotDTO | None = await bot_gate.get_bot_by_id(bot.id)
    if bot_info is None:
        return
    if bot_info.status != 'active':
        return

    await send_message(
        bot=bot,
        message=message,
        chat_id=bot_info.chat_id,
        thread_id=bot_info.thread_id
    )

    await message.reply('Ваше сообщение передано в редакцию. Спасибо за обращение ☺️')