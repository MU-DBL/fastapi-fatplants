from sqlalchemy.ext.asyncio import create_async_engine

# from auth.credentials import db_credentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


async_engine = None


async def get_async_session() -> AsyncSession:

    async_session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


# def get_async_engine():
#     try:
#         # SQLALCHEMY_DATABASE_URL = (
#         #     "mysql+asyncmy://{user}:{password}@{host}:{port}/{db}".format(
#         #         **db_credentials
#         #     )
#         # )
#         engine = create_async_engine(
#             SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0, pool_pre_ping=True
#         )
#         return engine
#     except Exception as e:
#         print("Error connecting to database: {}".format(e))
#         return None
