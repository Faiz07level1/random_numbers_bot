import asyncio
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
import random
from aiogram.filters import Command
from app.keyboard import story_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from app.database.requests import update_all_stickers_by_username ,get_games_by_username, get_sticker_by_product, update_your_sticker_by_username, get_story
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()
class Product(StatesGroup):
    product = State()


router = Router()

@router.callback_query(F.data.startswith("product_"))
async def buy_product(callback: CallbackQuery):
    product = callback.data.split("_")[1]
    sticker_data = await get_sticker_by_product(product)
    products = await get_story()
    games = await get_games_by_username(callback.from_user.username)
    if not games.all_stickers or product not in games.all_stickers.split(",") :
        if games.money >= sticker_data.sticker_price:
            if (games.all_stickers):
                # print(games.all_stickers)
                await update_all_stickers_by_username(username=callback.from_user.username, all_stickers=games.all_stickers+f",{product}", money=games.money-sticker_data.sticker_price)
                games = await get_games_by_username(callback.from_user.username)
                
                # if (len(games.all_stickers.split(",")) == len(products.all())):
                #     print("ыыы")
                #     await callback.message.delete()
                #     await callback.message.answer("Вы купили все стикеры из магазина")
                # else:
                await callback.message.edit_text(F"Вы купили новый стикер - {sticker_data.sticker}", reply_markup=await story_keyboard(products=products, games=games))
                
            else:
                await update_all_stickers_by_username(username=callback.from_user.username, all_stickers=product, money=games.money-sticker_data.sticker_price)
                await update_your_sticker_by_username(username=callback.from_user.username, sticker=sticker_data.sticker)
                games = await get_games_by_username(callback.from_user.username)
                await callback.message.edit_text(F"Вы купили первый стикер - {sticker_data.sticker}", reply_markup=await story_keyboard(products=products, games=games))
        else:
            await callback.message.edit_text('Извините но у вас недостаточно 🤑\n'
                                             F"Сейчас у вас {games.money}🤑")
    else:
        await callback.message.edit_text('Извините но вы уже купили этот стикер')
    
    
@router.callback_query(F.data.startswith("user_sticker_"))
async def buy_product(callback: CallbackQuery):
    product = callback.data.split("_")[2]
    sticker_data = await get_sticker_by_product(product)
    await update_your_sticker_by_username(username=callback.from_user.username, sticker=sticker_data.sticker)
    await callback.message.delete()
    await callback.message.answer(F"Вы выбрали {sticker_data.sticker} стикер из вашей колекции")        

  

