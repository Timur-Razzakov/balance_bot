from typing import Union

from decouple import config
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine as _create_async_engine


def create_async_engine(url: Union[str, URL]) -> AsyncEngine:
    return _create_async_engine(
        url=url,
        echo=config("DEBUG", cast=bool, default=False),
        pool_pre_ping=True,
    )
