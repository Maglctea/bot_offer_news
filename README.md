# Bot offer news
<hr/>

## Preparation
1. Fill in .env
<hr/>

### Start app in docker
Enter the following command from the root of the project
```bash
docker-compose up -d
```

### Start app in local
1. Create database
2. Enter the following commands from the root of the project
    ```bash
    pip install -e .
    alembic upgrade head
    python -m bot_offer_news
    python -m bot_offer_news.api
    ```
