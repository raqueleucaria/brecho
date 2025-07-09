# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry

from src.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


table_registry = registry()


# modificando o get_session para usar AsyncSession
#  que é compatível com operações assíncronas
# "expire_on_commit=False":
# é usado para evitar que os objetos sejam expirados após o commit
# permitindo que sejam usados imediatamente após a transação
# evitando novas consultas ao banco de dados para acessar os mesmos objetos.
