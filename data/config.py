from pathlib import Path
from decouple import config
from sqlalchemy import URL

PROJECT_ROOT = Path(__file__).parent.parent

BOT_TOKEN = config("BOT_TOKEN")
print(23423432423, BOT_TOKEN)

ADMIN_ID = list(
    map(int, config("ADMINS_ID").strip("[]").split(","))
)

DB_USER = config("POSTGRES_USER")
DB_PASS = config("POSTGRES_PASSWORD")
DB_NAME = config("POSTGRES_DB")
DB_HOST = config("POSTGRES_HOST")
DB_PORT = config("POSTGRES_PORT", cast=int)

DB_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)
