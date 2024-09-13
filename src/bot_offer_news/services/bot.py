from asyncio import gather

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from dishka import FromDishka

from bot_offer_news.db.gate.bot import BotGateway
from bot_offer_news.dto.bot import BotDTO
from bot_offer_news.utils.bot import create_bot_webhook, delete_bot_webhook


async def create_bot_webhooks(bot_gate: FromDishka[BotGateway]) -> None:
    bots_dto: list[BotDTO] = await bot_gate.get_all_bots()
    for bot_dto in bots_dto:
        bot: Bot = Bot(bot_dto.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await create_bot_webhook(bot)


async def clear_bot_webhooks(bot_gate: FromDishka[BotGateway]) -> None:
    bots_dto: list[BotDTO] = await bot_gate.get_all_bots()
    for bot_dto in bots_dto:
        bot: Bot = Bot(bot_dto.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await delete_bot_webhook(bot)


async def update_bot_webhooks(bot_gate: FromDishka[BotGateway]) -> None:
    await gather(
        clear_bot_webhooks(bot_gate),
        create_bot_webhooks(bot_gate)
    )


async def send_message(bot: Bot, message: Message, chat_id: int, thread_id: int = None):
    if message.photo:
        await bot.send_photo(
            chat_id=chat_id,
            message_thread_id=thread_id,
            photo=message.photo[-1].file_id,
            caption=message.md_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif message.document:
        await bot.send_document(
            chat_id=chat_id,
            message_thread_id=thread_id,
            document=message.document.file_id,
            caption=message.md_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif message.video:
        await bot.send_video(
            chat_id=chat_id,
            message_thread_id=thread_id,
            video=message.video.file_id,
            caption=message.md_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif message.audio:
        await bot.send_audio(
            chat_id=chat_id,
            message_thread_id=thread_id,
            audio=message.audio.file_id,
            caption=message.md_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif message.voice:
        await bot.send_voice(
            chat_id=chat_id,
            message_thread_id=thread_id,
            voice=message.voice.file_id,
            caption=message.md_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif message.video_note:
        await bot.send_video_note(
            chat_id=chat_id,
            message_thread_id=thread_id,
            video_note=message.video_note.file_id,
        )
    elif message.sticker:
        await bot.send_sticker(
            chat_id=chat_id,
            message_thread_id=thread_id,
            sticker=message.sticker.file_id
        )
    elif message.text:
        await bot.send_message(
            chat_id=chat_id,
            message_thread_id=thread_id,
            text=message.md_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        await message.reply(text='Недопустимый вид сообщения')
