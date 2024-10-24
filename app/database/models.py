
from typing import Optional
from sqlalchemy import BigInteger, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession



engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")


async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(80))
    username: Mapped[str] = mapped_column(String(50))


class Rank(Base):
    __tablename__ = "rank"
    id: Mapped[int] = mapped_column(primary_key=True)
    wins: Mapped[int] = mapped_column(Integer)
    rank: Mapped[str] = mapped_column(String(50))


class Story(Base):
    __tablename__ = "story"
    id: Mapped[int] = mapped_column(primary_key=True)
    sticker: Mapped[str] = mapped_column(String(5))
    sticker_name: Mapped[str] = mapped_column(String(50))
    sticker_price: Mapped[int] = mapped_column(Integer)
    
    
    

class Game_len(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    total_games: Mapped[int] = mapped_column(Integer)
    wins: Mapped[int] = mapped_column(Integer)
    in_game: Mapped[str] = mapped_column(String(10))
    game_numbers: Mapped[int] = mapped_column(Integer, default=0)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    crystals: Mapped[int] = mapped_column(Integer, default=0)
    money: Mapped[int] = mapped_column(Integer, default=0)
    goblet: Mapped[int] = mapped_column(Integer, default=0)
    sticker: Mapped[str] = mapped_column(String(2000), nullable=True)
    all_stickers: Mapped[str] = mapped_column(String(2000), nullable=True)
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)