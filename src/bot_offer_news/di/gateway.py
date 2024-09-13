from dishka import Provider, Scope, provide

from bot_offer_news.db.gate.bot import BotGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    bot_gateway = provide(source=BotGateway)
