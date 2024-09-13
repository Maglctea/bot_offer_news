from bot_offer_news import settings


def get_full_db_url() -> str:
    return f"{settings.DB_TYPE}+{settings.DB_DRIVER}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
