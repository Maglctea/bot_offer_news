from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from bot_offer_news.utils.db import get_full_db_url


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(
            url=get_full_db_url(),
            echo=True,
            pool_size=10,
        )
        yield engine
        await engine.dispose(True)

    @provide
    def create_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        session_factory = async_sessionmaker(
            bind=engine,
        )
        return session_factory

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_factory() as session:
            yield session
