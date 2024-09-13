from dataclasses import dataclass


@dataclass
class BotDTO:
    bot_id: int
    chat_id: int
    thread_id: int
    token: str
    status: str


@dataclass
class BotResponseDTO:
    bot_id: int
    chat_id: int
    thread_id: int
    status: str
