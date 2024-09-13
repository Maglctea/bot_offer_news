import asyncio
import logging

from aiogram import Dispatcher, Bot

import settings
from routers import router

logging.basicConfig(level=logging.INFO)


def main():
    dp = Dispatcher()

    dp.include_router(router)

    bot: Bot = Bot(settings.BOT_TOKEN)

    dp.run_polling(bot)


if __name__ == '__main__':
    main()
