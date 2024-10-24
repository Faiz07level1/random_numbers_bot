import asyncio
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
import random
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from app.keyboard import keyboard_1, my_keyboard, kb_builder, rate_keyboard, exchange_keyboard, story_keyboard, user_sticker
from app.database.requests import set_games, set_user, get_games_by_username, update_games_by_username, \
                                    update_in_games_by_username, get_games, update_attempts_by_username, update_crystals_by_username, get_ranks, get_story
from app.my_func import gamers_statistic, get_rank, rank_clasification

import datetime
# Количество попыток, доступных пользователю в игре
ATTEMPTS = 6




# Словарь, в котором будут храниться данные пользователя

def get_random_number() -> int:
    return random.randint(1, 100)

router = Router()


class User(StatesGroup):
    secret_number = State()
    attempts = State()

# class Params(StatesGroup):
#     wb_api_token = State()
#     api_link = State()
#     client_comand = State()
#     params = State()
#     params_1 = State()
#     params_2 = State()
#     params_3 = State()
#     category_content = State()
# Этот хэндлер будет срабатывать на команду "/start"
@router.message(F.text == "/start")
async def process_start_command(message: Message):
    await set_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await set_games(username=message.from_user.username, in_game="False")
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help',
        reply_markup=keyboard_1
    )


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?',
        reply_markup=keyboard_1
    )


# Этот хэндлер будет срабатывать на команду "/stat"
@router.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    games = await get_games_by_username(message.from_user.username)
    ranks = await get_ranks()
    rank = await get_rank(wins=games.wins, ranks=ranks)
    await message.answer(
        f"Ранг игрока: {rank}\n\n"
        f'Всего игр сыграно: {games.total_games}\n\n'
        f'Игр выиграно: {games.wins}\n\n'
        f"манипупсиков: {games.money}🤑\n\n"
        f"кубков: {games.goblet}🏆\n\n"
        f"кристалов: {games.crystals}💎\n\n",
        reply_markup=keyboard_1
    )

@router.message(Command(commands='gamer'))
async def process_stat_command(message: Message):
    gamers = await get_games()

    ranks = await get_ranks()
    gamers_stat = await asyncio.create_task(gamers_statistic(gamers=gamers, ranks=ranks))
    await message.answer(gamers_stat, reply_markup=keyboard_1)

@router.message(Command(commands='my_stickers'))
async def process_stat_command(message: Message):
    gamers = await get_games()

    
    
    
    
    
# Этот хэндлер будет срабатывать на команду "/cancel"
@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    games = await get_games_by_username(message.from_user.username)
    if games.in_game == "True":
        
        await update_games_by_username(username=message.from_user.username, total_games=games.total_games+1, wins=None, in_game="False", game_numbers=0, money=games.money)
        await update_attempts_by_username(username=message.from_user.username, attempts=0)
        await state.clear()
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом',
            reply_markup=keyboard_1
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )
        
        
@router.message(Command("rate"))
async def rate(message: Message):
    await message.answer("Вы зашли на ставки\n"
                         "Правила ставок:\n"
                         "Вы можете поставить ставку в манипупсиках\n"
                         "Если вы хотите поставить ставку то нажмите ставка\n"
                         "Если же вы зассали нажмите отменить\n"
                         "Если вы нажали ставка то введите количество манипупсиков\n"
                         "максимальное число 50\n"
                         "ставки происходят при помощи игры камень ножницы бумага\n"
                         "приз вы получаете один к одному, ну и за поражение минусуется введенная сумма",
                         reply_markup=rate_keyboard)
    
@router.message(Command("ranks"))
async def rate(message: Message):
    ranks = await get_ranks()
    ranks_info = await rank_clasification(ranks=ranks)
    await message.answer(ranks_info)
    
@router.message(Command("exchange"))
async def rate(message: Message):
    await message.answer("Вы зашли на обмен\n"
                         "Правила обмена:\n"
                         "вы можете поменять кубки или кристалы на манипупсики\n"
                         "1💎 равен 750🤑 один 🏆 равен 30🤑\n"
                         "Если вы передумали менять нажмите отменить",
                         reply_markup=exchange_keyboard)

@router.callback_query(F.data == "cancel")
async def cancel_all(callback_data: CallbackQuery):
    await callback_data.message.answer("Вы нажали отменить\n"
                                          "Давайте сыграем в\n"
                                          "игру: угадай число",
                                          reply_markup=keyboard_1)
    
@router.message(Command("story"))
async def rate(message: Message):
    products = await get_story()
    games = await get_games_by_username(username=message.from_user.username)
    await message.answer("Вы зашли в магазин", reply_markup=await story_keyboard(products=products, games=games))

@router.message(Command("my_collection"))
async def rate(message: Message):
    products = await get_story()
    games = await get_games_by_username(username=message.from_user.username)
    if not games.all_stickers:
        await message.answer("Извините, но у вас нету стикеров")
    elif games.all_stickers and games.all_stickers.find(",") == -1:
        await message.answer("Извините, но чтобы открыть колекцию\n"
                             "нужно купить минимум два стикера\n"
                             F"сейчас у вас есть один стикер - {games.sticker}")
    else:
        await message.answer("Вы зашли в вашу колекцию,\n"
                         "Выберите нужный вам стикер", reply_markup=await user_sticker(products=products, all_stickers=games.all_stickers))



# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@router.message(F.text.lower().in_(['да', 'давай сыграем', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message, state: FSMContext):
    games = await get_games_by_username(message.from_user.username)
    if games.in_game == "False":
        await update_in_games_by_username(username=message.from_user.username, in_game="True", game_numbers=get_random_number(), attempts=ATTEMPTS)
        await get_games_by_username(username=message.from_user.username)
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!',
            reply_markup=my_keyboard.as_markup(resize_keyboard=True, input_field_placeholder="Введите число")
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@router.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    games = await get_games_by_username(message.from_user.username)
    if games.in_game == "False":
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message, state: FSMContext):
    games = await get_games_by_username(message.from_user.username)
    if games.in_game == "True":
        if int(message.text) == games.game_numbers:
            await update_games_by_username(username=message.from_user.username, total_games=games.total_games+1, wins=games.wins+1, in_game="False", game_numbers=0, money=games.money+(games.attempts-1)*10, goblet=games.goblet+1)
            await update_attempts_by_username(username=message.from_user.username, attempts=0)
            if games.attempts == 6:
                await update_crystals_by_username(username=message.from_user.username, crystals=games.crystals+1)

            await message.answer(
                F'Ура!!! Вы угадали число!\n\n'
                F"{F"Вы выйграли {(games.attempts-1)*10}🤑\n" if games.attempts==6 else F"Вы выйграли {(games.attempts-1)*10}🤑\n\n"}"
                F"{"Вы выйграли 1💎\n\n" if games.attempts==6 else ""}"
                'Может, сыграем еще?',
                reply_markup=keyboard_1
            )
        else:
            await update_attempts_by_username(username=message.from_user.username, attempts=games.attempts-1)
            if games.attempts <= 1 and games.in_game == "True":
                if games.money>20 and games.goblet>1:
                    await update_games_by_username(username=message.from_user.username, total_games=games.total_games+1, wins=None, in_game="False", game_numbers=0, money=games.money-20, goblet=games.goblet-1)
                elif games.money>20 and games.goblet<1:
                    await update_games_by_username(username=message.from_user.username, total_games=games.total_games+1, wins=None, in_game="False", game_numbers=0, money=games.money-20, goblet=games.goblet)
                elif games.money<20 and games.goblet>1:
                    await update_games_by_username(username=message.from_user.username, total_games=games.total_games+1, wins=None, in_game="False", game_numbers=0, money=0, goblet=games.goblet-1)
                elif games.money<20 and games.goblet<1:
                    await update_games_by_username(username=message.from_user.username, total_games=games.total_games+1, wins=None, in_game="False", game_numbers=0, money=0, goblet=games.goblet)
                
                await message.answer(
                    f'К сожалению, у вас больше не осталось '
                    f'попыток. Вы проиграли 20🤑 - у вас осталось {games.money-20} :(\n\nМое число '
                    f'было {games.game_numbers}\n\nДавайте '
                    f'сыграем еще?',
                    reply_markup=keyboard_1
                )
            elif int(message.text) > games.game_numbers:    

                await message.answer('Мое число меньше')
            elif int(message.text) < games.game_numbers:
                # await update_attempts_by_username(username=message.from_user.username, attempts=games.attempts-1)
                await message.answer('Мое число больше')
            
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@router.message()
async def process_other_answers(message: Message, state: FSMContext):
    games = await get_games_by_username(message.from_user.username)
    if games.in_game == "True":
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )
