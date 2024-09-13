import asyncio

import uvicorn
from aiogram import Bot
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka, inject, FromDishka
from fastapi import FastAPI, Body, status, Form
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from bot_offer_news import settings
from bot_offer_news.db.gate.bot import BotGateway
from bot_offer_news.di.db import DbProvider
from bot_offer_news.di.gateway import GatewayProvider
from bot_offer_news.dto.bot import BotDTO, BotResponseDTO
from bot_offer_news.utils.bot import create_bot_webhook, delete_bot_webhook, delete_bot_action, add_bot_action

app = FastAPI(root_path='/api')


@app.post('/bots', status_code=status.HTTP_201_CREATED)
@inject
async def add_bot(
        bot_gate: FromDishka[BotGateway],
        chat_id: int = Body(),
        thread_id: int = Body(),
        token: str = Body()
):
    bot: Bot = await add_bot_action(bot_gate, chat_id, thread_id, token)
    return {'bot_id': bot.id}


@app.get('/bots', status_code=status.HTTP_200_OK)
@inject
async def get_all_bots(
        bot_gate: FromDishka[BotGateway],
) -> list[BotResponseDTO]:
    bots: list[BotDTO] = await bot_gate.get_all_bots()
    await bot_gate.commit()

    return [BotResponseDTO(bot_id=bot.bot_id, chat_id=bot.chat_id, thread_id=bot.thread_id, status=bot.status) for bot in bots]


@app.delete('/bots/{bot_id}', status_code=status.HTTP_200_OK)
@inject
async def delete_bot(
        bot_gate: FromDishka[BotGateway],
        bot_id: int
):
    await delete_bot_action(bot_gate, bot_id)
    return 'OK'


@app.post('/bots/{bot_id}/start')
@inject
async def start_bot(bot_id: int, bot_gate: FromDishka[BotGateway]):
    bot_info = await bot_gate.get_bot_by_id(bot_id)
    await bot_gate.update_bot_status(bot_id, 'active')

    await bot_gate.commit()
    bot = Bot(bot_info.token)

    await create_bot_webhook(bot)
    await bot.session.close()
    return 'OK'


@app.post('/bots/{bot_id}/stop')
@inject
async def stop_bot(bot_id: int, bot_gate: FromDishka[BotGateway]):
    bot_info = await bot_gate.get_bot_by_id(bot_id)
    await bot_gate.update_bot_status(bot_id, 'inactive')

    bot = Bot(bot_info.token)
    await asyncio.gather(
        bot_gate.commit(),
        delete_bot_webhook(bot)
    )

    await bot.session.close()
    return "OK"


app.mount("/static", StaticFiles(directory='/static', html=True), name="static")


@app.post("/webapp/add_bot_form", response_class=HTMLResponse)
@inject
async def add_bot_form(
        bot_gate: FromDishka[BotGateway],
        chat_id: int = Form(...),
        thread_id: int = Form(...),
        token: str = Form(...)
):
    await add_bot_action(bot_gate, chat_id, thread_id, token)
    return RedirectResponse(url=f"{settings.API_URL}/api/static/action_complete.html", status_code=303)


@app.post("/webapp/delete_bot_form", response_class=HTMLResponse)
@inject
async def delete_bot_form(
        bot_gate: FromDishka[BotGateway],
        bot_id: int = Form(...),
):
    await delete_bot_action(bot_gate, bot_id)
    return RedirectResponse(url=f"{settings.API_URL}/api/static/action_complete.html", status_code=303)


def main():
    container = make_async_container(
        DbProvider(),
        GatewayProvider(),
    )
    setup_dishka(
        container=container,
        app=app,
    )
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
