from app.database.models import async_session, Game_len, User, Rank, Story
from sqlalchemy import select, update

async def get_games_by_username(username):
    async with async_session() as session:
        return await session.scalar(select(Game_len).where(Game_len.username==username))

async def set_user(tg_id, name, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, name=name, username=username))
            await session.commit()

async def get_user(username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))
        
        return user

async def set_games(username, in_game):
    async with async_session() as session:
        games = await session.scalar(select(Game_len).where(Game_len.username == username))
        if not games:
            session.add(Game_len(total_games=0, wins=0, username=username, in_game=in_game))
            await session.commit()

async def update_games_by_username(username, total_games, wins, in_game, game_numbers, money, goblet):
    async with async_session() as session:
        if wins:
            await session.execute(update(Game_len).where(Game_len.username == username).values(total_games=total_games, wins=wins, in_game=in_game, game_numbers=game_numbers, money=money, goblet=goblet))
        else:
            await session.execute(update(Game_len).where(Game_len.username == username).values(total_games=total_games, in_game=in_game, game_numbers=game_numbers, money=money, goblet=goblet))
        await session.commit()


async def update_in_games_by_username(username, in_game, game_numbers, attempts):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(in_game=in_game, game_numbers=game_numbers, attempts=attempts))
        await session.commit()

async def update_money_by_username(username, money):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(money=money))
        await session.commit()

async def update_attempts_by_username(username, attempts):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(attempts=attempts))
        await session.commit()

async def update_crystals_by_username(username, crystals):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(crystals=crystals))
        await session.commit()

async def update_crystals_and_money_by_username(username, crystals, money):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(crystals=crystals, money=money))
        await session.commit()

async def update_goblet_and_money_by_username(username, goblet, money):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(goblet=goblet, money=money))
        await session.commit()

async def get_games():
    async with async_session() as session:
        return await session.scalars(select(Game_len).order_by(Game_len.wins))
    
async def get_ranks():
    async with async_session() as session:
        return await session.scalars(select(Rank).order_by(Rank.wins))
    
async def get_story():
    async with async_session() as session:
        return await session.scalars(select(Story))
    
async def update_all_stickers_by_username(username, all_stickers, money):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(all_stickers=all_stickers, money=money))
        await session.commit()
    

async def get_sticker_by_product(sticker_name):
    async with async_session() as session:
        return await session.scalar(select(Story).where(Story.sticker_name==sticker_name))
    
async def update_your_sticker_by_username(username, sticker):
    async with async_session() as session:
        await session.execute(update(Game_len).where(Game_len.username == username).values(sticker=sticker))
        await session.commit()
    




