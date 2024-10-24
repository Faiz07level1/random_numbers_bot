import asyncio
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
import random
from aiogram.filters import Command
from app.keyboard import rate_keyboard, keyboard_1, my_inline_button, exchange_keyboard_ok, exchange_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from app.database.requests import update_crystals_and_money_by_username, update_goblet_and_money_by_username, get_games_by_username

class Exchange(StatesGroup):
    ex_crystals = State()
    ex_goblet = State()
    exchange_on = State()

router = Router()

@router.callback_query(F.data=="exchange_ok")
async def exchange_ok(callback_data: CallbackQuery, state: FSMContext):
       data = await state.get_data()
       await state.clear()
       games = await get_games_by_username(callback_data.from_user.username)
       if data["exchange_on"] == "crystals":
           await update_crystals_and_money_by_username(callback_data.from_user.username, crystals=games.crystals-1, money=games.money+750)
           await callback_data.message.answer(F"У вас было {games.crystals}💎 теперь у вас {games.crystals-1}💎\n"
                                              F"У вас было {games.money}🤑 теперь у вас {games.money+750}🤑\n")
       if data["exchange_on"] == "wins":
           await update_goblet_and_money_by_username(callback_data.from_user.username, goblet=games.goblet-data["ex_goblet"], money=games.money+30*data["ex_goblet"])
           await callback_data.message.answer(F"У вас было {games.goblet}🏆 теперь у вас {games.goblet-data['ex_goblet']}🏆\n"
                                              F"У вас было {games.money}🤑 теперь у вас {games.money+30*data["ex_goblet"]}🤑\n")

@router.callback_query(F.data.startswith("exchange"))
async def exchange_message(callback_data: CallbackQuery, state: FSMContext):
    data_message = callback_data.data.split("_")[1]
    games = await get_games_by_username(callback_data.from_user.username)
    if data_message == "crystals":
        if games.crystals < 1:
            await callback_data.message.answer("Извините но у вас 0💎")
            await callback_data.message.answer("вы можете попробовать поменять на кубки\n"
                                               "нажмите /exchange")
        else:
            await state.update_data(exchange_on=data_message)
            await callback_data.message.answer("Вы выбрали обмен на кристал\n" 
                                            "Вы меняете 1💎 на 750🤑")
            await callback_data.message.answer("Пожалуйста подтвердите ваш обмен\n"
                                    "и нажмите обмен или если вы\n"
                                    "передумали нажмите отмена", reply_markup=exchange_keyboard_ok)

    elif data_message == "wins":
        await state.update_data(exchange_on=data_message)
        await state.set_state(Exchange.ex_goblet)
        await callback_data.message.answer("Вы выбрали обмен на кубки\n\n"
                                           "Пожалуйста введите число кубки для обмена")
        
           

@router.message(Exchange.ex_goblet)
async def exchange_wins(message: Message, state: FSMContext):
    if message.text.isdigit() == False:
        await state.set_state(Exchange.ex_goblet)
        await message.answer("Вы ввели некоректные данные\n"
                             "Пожалуйста попробуйте еще раз")
        
    else:
        await state.update_data(ex_goblet=int(message.text))
        data = await state.get_data()
        games = await get_games_by_username(message.from_user.username)
        if games.goblet < 1:
            await state.clear()
            await message.answer(F"Извините но у вас нету {data["ex_goblet"]} сейчас у вас есть {games.goblet} кубков")
            await message.answer("вы можете попробовать поменять на кристалы\n"
                                               "нажмите /exchange")
        else:
            if data["ex_goblet"] > games.goblet:
                await state.set_state(Exchange.ex_goblet)
                await message.answer(F"Извините но у вас нету {data["ex_goblet"]}🏆 сейчас максимум что вы можете поставить это {games.goblet} кубков")
                await message.answer(F"Пожалуйста введите правильное количество")

            else:
                await state.update_data(ex_goblet=int(message.text))
                data = await state.get_data()
                if data["ex_goblet"] > 20:
                    await state.set_state(Exchange.ex_goblet)
                    await message.answer("Вы ввели число больше 20-максимального\n"
                                    "Пожалуйста попробуйте еще раз")
                if data["ex_goblet"] < 1:
                    await state.set_state(Exchange.ex_goblet)
                    await message.answer("Вы ввели число меньше 1-минимального\n"
                                    "Пожалуйста попробуйте еще раз")
                else:
                    await message.answer(F"Вы меняете {data["ex_goblet"]}🏆 на {data["ex_goblet"]*30}🤑")
                    await message.answer("Пожалуйста подтвердите ваш обмен\n"
                                        "и нажмите обмен или если вы\n"
                                        "передумали нажмите отмена", reply_markup=exchange_keyboard_ok)




