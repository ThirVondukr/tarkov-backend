from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import settings

engine = create_async_engine(settings.database.url, future=True)
Session = sessionmaker(bind=engine, class_=AsyncSession, future=True)
Base = declarative_base()
