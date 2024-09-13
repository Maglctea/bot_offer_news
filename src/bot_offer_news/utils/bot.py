import logging
from asyncio import gather

from aiogram import Bot
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from bot_offer_news import settings
from bot_offer_news.db.gate.bot import BotGateway
from bot_offer_news.dto.bot import BotDTO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def delete_bot_action(
        bot_gate: BotGateway,
        bot_id: int
) -> None:
    bot_dto: BotDTO = await bot_gate.get_bot_by_id(bot_id)
    bot: Bot = Bot(token=bot_dto.token)
    await delete_bot_webhook(bot)
    await bot_gate.delete_server(bot_id)
    await bot_gate.commit()


async def add_bot_action(
        bot_gate: BotGateway,
        chat_id: int,
        thread_id: int,
        token: str,
) -> Bot:
    try:
        await bot_gate.add_bot(chat_id, thread_id, token)
        await bot_gate.commit()
    except IntegrityError as e:
        if 'already exist' in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bot already exist')

    bot = Bot(token)
    await create_bot_webhook(bot)
    await bot.session.close()
    return bot


async def create_bot_webhook(bot: Bot) -> None:
    path: str = f'{settings.WEBHOOK_URL}/webhook/{bot.token}'
    user, _ = await gather(
        bot.get_me(),
        bot.set_webhook(path, secret_token=settings.WEBHOOK_SECRET_KEY)
    )
    logger.info(f'Bot {user.username} registered')


async def delete_bot_webhook(bot: Bot) -> None:
    user, _ = await gather(
        bot.get_me(),
        bot.delete_webhook()
    )
    logger.info(f'Bot {user.username} deleted')

# class BotIdBasedRequestHandler(BaseRequestHandler):
#     def __init__(
#             self,
#             dispatcher: Dispatcher,
#             handle_in_background: bool = True,
#             bot_settings: Optional[Dict[str, Any]] = None,
#             **data: Any,
#     ) -> None:
#         """
#         Handler that supports multiple bots the context will be resolved
#         from path variable 'bot_token'
#
#         .. note::
#
#             This handler is not recommended in due to token is available in URL
#             and can be logged by reverse proxy server or other middleware.
#
#         :param dispatcher: instance of :class:`aiogram.dispatcher.dispatcher.Dispatcher`
#         :param handle_in_background: immediately responds to the Telegram instead of
#             a waiting end of handler process
#         :param bot_settings: kwargs that will be passed to new Bot instance
#         """
#         super().__init__(dispatcher=dispatcher, handle_in_background=handle_in_background, **data)
#         if bot_settings is None:
#             bot_settings = {}
#         self.bot_settings = bot_settings
#         self.bots: Dict[int, Bot] = {}
#
#     def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
#         return True
#
#     def add_bot(self, bot: Bot):
#         self.bots[bot.id] = bot
#
#     async def close(self) -> None:
#         for bot in self.bots.values():
#             await bot.session.close()
#
#     def register(self, app: Application, /, path: str, **kwargs: Any) -> None:
#         """
#         Validate path, register route and shutdown callback
#
#         :param app: instance of aiohttp Application
#         :param path: route path
#         :param kwargs:
#         """
#         if "{bot_id}" not in path:
#             raise ValueError("Path should contains '{bot_token}' substring")
#         super().register(app, path=path, **kwargs)
#
#     async def resolve_bot(self, request: web.Request) -> Bot:
#         """
#         Get bot token from a path and create or get from cache Bot instance
#
#         :param request:
#         :return:
#         """
#         token = request.match_info["bot_id"]
#         if token not in self.bots:
#             self.bots[token] = Bot(token=token, **self.bot_settings)
#         return self.bots[token]
