from sqlalchemy.ext.asyncio import AsyncSession


class BaseGateway:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def commit(self) -> None:
        await self.session.commit()
        await self.session.close()
