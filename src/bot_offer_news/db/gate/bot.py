from sqlalchemy import select, Select, update, Update, delete
from sqlalchemy.orm.exc import NoResultFound

from bot_offer_news.db.gate.base import BaseGateway
from bot_offer_news.db.models import BotModel
from bot_offer_news.dto.bot import BotDTO


class BotGateway(BaseGateway):
    async def get_bot_by_id(self, bot_id: int) -> BotDTO | None:
        try:
            bot: BotModel = await self.session.get_one(BotModel, bot_id)
            return bot.to_dto()
        except NoResultFound:
            return None

    async def add_bot(self, chat_id: int, thread_id, token: str) -> None:
        bot_id: int = int(token.split(':')[0])
        bot = BotModel(bot_id=bot_id, chat_id=chat_id, thread_id=thread_id, token=token)
        self.session.add(bot)
        await self.session.flush()

    async def update_bot_status(self, bot_id: int, new_status: str) -> None:
        smtp: Update = (
            update(BotModel)
            .values(status=new_status)
            .where(BotModel.bot_id == bot_id)
        )
        await self.session.execute(smtp)
        await self.session.flush()

    async def get_all_bots(self) -> list[BotDTO]:
        stmt: Select = select(BotModel)
        bots: list[BotModel] = list(await self.session.scalars(stmt))

        bots: list[BotDTO] = [
            bot.to_dto()
            for bot in bots
        ]
        return bots

    async def delete_server(
            self,
            bot_id: int
    ):
        stmt = delete(BotModel).where(BotModel.bot_id == bot_id)
        await self.session.execute(stmt)
