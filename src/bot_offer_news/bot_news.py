import logging

from aiogram import Dispatcher
from aiogram.webhook.aiohttp_server import TokenBasedRequestHandler
from aiohttp import web
from aiohttp.web import Application
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from bot_offer_news.di.db import DbProvider
from bot_offer_news.di.gateway import GatewayProvider
from bot_offer_news.routers.info import info_router
from bot_offer_news.routers.news import news_router
from bot_offer_news.services.bot import update_bot_webhooks, clear_bot_webhooks

logging.basicConfig(level=logging.INFO)


def main():
    dp = Dispatcher()

    container = make_async_container(
        DbProvider(),
        GatewayProvider(),
    )
    setup_dishka(
        container=container,
        router=dp,
        auto_inject=True
    )

    dp.include_router(info_router)
    dp.include_router(news_router)
    dp.shutdown.register(clear_bot_webhooks)
    dp.startup.register(update_bot_webhooks)

    web_app = Application()

    webhook_requests_handler: TokenBasedRequestHandler = TokenBasedRequestHandler(dispatcher=dp)
    webhook_requests_handler.register(web_app, '/webhook/{bot_token}')

    web.run_app(
        app=web_app,
        host='0.0.0.0',
        port=8000
    )


if __name__ == '__main__':
    main()
