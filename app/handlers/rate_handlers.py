

import asyncio
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
import random
from aiogram.filters import Command
from app.keyboard import rate_keyboard, keyboard_1, my_inline_button
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from app.database.requests import update_money_by_username, get_games_by_username

router = Router()

class Rate(StatesGroup):
    rate_num = State()

movements = ["Камень", "Ножницы", "Бумага"]
lexicon = {"scissors": "Ножницы", "paper": "Бумага", "rock": "Камень"}
async def get_random_meaning() -> str:
    return random.choice(movements)


@router.callback_query(F.data == "rate")
async def rate_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Rate.rate_num)
    await callback.message.answer("Введите вашу ставку от 1 до 50")

@router.message(Rate.rate_num)
async def rate_start(message: Message, state: FSMContext):
    games = await get_games_by_username(message.from_user.username)
    
        
    if message.text.isdigit():
        await state.update_data(rate_num=int(message.text))
        data = await state.get_data()
        if data["rate_num"] > games.money:
            await message.answer("Извините, на данный момент у вас нету столько манипупсиков\n"
                                 F"Максимальную ставку которую вы сейчас можете поставить это {games.money}🤑")
        else:
            if (data["rate_num"] > 50):
                await state.set_state(Rate.rate_num)
                await message.answer("Вы ввели число больше 50")
                await message.answer("Пожалуйста введите правильное число")
            elif (data["rate_num"] < 1):
                await state.set_state(Rate.rate_num)
                await message.answer("Вы ввели число меньше 1")
                await message.answer("Пожалуйста введите правильное число")
            else:
                await message.answer("Ставка поставлена\n"
                                    "Давайте поиграем в игру камень-ножницы-бумага", reply_markup=my_inline_button)

    else:
        await state.set_state(Rate.rate_num)
        await message.answer("Вы ввели некоректные данные\n"
                             "Пожалуйста попробуйте еще раз")
        await message.answer("Введите число")
        
        
# @router.message(F.data == "rock-paper-scissors")
# async def proposal_do(message: Message):
#     await message.answer('Отлично! Делай свой выбор!', reply_markup=my_inline_button)



@router.callback_query((F.data.in_(["scissors","paper","rock"])))
async def start_bot(callback: CallbackQuery, state: FSMContext):
    meaning = await asyncio.create_task(get_random_meaning())
    games = await get_games_by_username(callback.from_user.username)
    data = await state.get_data()
    await state.clear()
    if (lexicon[callback.data] == meaning):
        await callback.message.answer(F"Вы выбрали {lexicon[callback.data]}")
        await state.set_state(Rate.rate_num)
        await callback.message.answer("Ничья\n"
                                      "Давай еще раз")
        await callback.message.answer("Введите ваше число")
    if (lexicon[callback.data] == "Камень"):
        if (meaning == "Бумага"):
            await update_money_by_username(username=callback.from_user.username, money=games.money-data["rate_num"])
            await callback.message.answer(F"Вы выбрали {lexicon[callback.data]}")
            await callback.message.answer(text=F"Вы проиграли, я выбрал {meaning}")
            await callback.message.answer(text=F"У вас было {games.money}🤑\n"
                                          F"Вы потеряли {data['rate_num']}🤑\n"
                                          F"У вас осталось {games.money-data['rate_num']}🤑", reply_markup=rate_keyboard)
        if (meaning == "Ножницы"):
            await update_money_by_username(username=callback.from_user.username, money=games.money+data["rate_num"])
            await callback.message.answer(F"Вы выбрали {lexicon[callback.data]}")
            await callback.message.answer(text=F"Вы выйграли, я выбрал {meaning}")
            await callback.message.answer(text=F"У вас было {games.money}🤑\n"
                                          F"Вы выйграли {data['rate_num']}🤑\n"
                                          F"У вас есть {games.money+data['rate_num']}🤑", reply_markup=rate_keyboard)
    if (lexicon[callback.data] == "Ножницы"):
        if (meaning == "Бумага"):
            await update_money_by_username(username=callback.from_user.username, money=games.money+data["rate_num"])
            await callback.message.answer(F"Вы выбрали {lexicon[callback.data]}")
            await callback.message.answer(text=F"Вы выйграли, я выбрал {meaning}")
            await callback.message.answer(text=F"У вас было {games.money}🤑\n"
                                          F"Вы выйграли {data['rate_num']}🤑\n"
                                          F"У вас есть {games.money+data['rate_num']}🤑", reply_markup=rate_keyboard)
        if (meaning == "Камень"):
            await update_money_by_username(username=callback.from_user.username, money=games.money-data["rate_num"])
            await callback.message.answer(F"Вы выбрали {lexicon[callback.data]}")
            await callback.message.answer(text=F"Вы проиграли, я выбрал {meaning}")
            await callback.message.answer(text=F"У вас было {games.money}🤑\n"
                                          F"Вы потеряли {data['rate_num']}🤑\n"
                                          F"У вас осталось {games.money-data['rate_num']}🤑", reply_markup=rate_keyboard)
    if (lexicon[callback.data] == "Бумага"):
        if (meaning == "Ножницы"):
            await update_money_by_username(username=callback.from_user.username, money=games.money-data["rate_num"])
            await callback.message.answer(F"Вы выбрали {lexicon[callback.data]}")
            await callback.message.answer(text=F"Вы проиграли, я выбрал {meaning}")
            await callback.message.answer(text=F"У вас было {games.money}\n"
                                          F"Вы потеряли {data['rate_num']}🤑\n"
                                          F"У вас осталось {games.money-data['rate_num']}🤑", reply_markup=rate_keyboard)
        if (meaning == "Камень"):
            await update_money_by_username(username=callback.from_user.username, money=games.money+data["rate_num"])
            await callback.message.answer(F"Вы выбрали {lexicon[callback.data]}")
            await callback.message.answer(text=F"Вы выйграли, я выбрал {meaning}")
            await callback.message.answer(text=F"У вас было {games.money}🤑\n"
                                          F"Вы выйграли {data['rate_num']}🤑\n"
                                          F"У вас есть {games.money+data['rate_num']}🤑", reply_markup=rate_keyboard)
    
    


    