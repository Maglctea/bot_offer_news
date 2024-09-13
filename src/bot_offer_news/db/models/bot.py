from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from bot_offer_news.db.models.base import Base
from bot_offer_news.dto.bot import BotDTO


class BotModel(Base):
    __tablename__ = "bot"
    bot_id: Mapped[int] = mapped_column(BigInteger(), unique=True, primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger())
    thread_id: Mapped[int]
    token: Mapped[str] = mapped_column(unique=True)
    status: Mapped[str] = mapped_column(default='active')

    def to_dto(self) -> BotDTO:
        return BotDTO(bot_id=self.bot_id, chat_id=self.chat_id, thread_id=self.thread_id, token=self.token, status=self.status)

    def __repr__(self) -> str:
        return fr"BotModel(bot_id={self.bot_id}, chat_id={self.chat_id}, thread_id={self.thread_id}, status={self.status})"
