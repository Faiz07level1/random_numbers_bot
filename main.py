
from environs import Env
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from app.handlers import rate_handlers, handlers, exchange_handlers, story_handlers
from app.database.models import async_main
from app.config_data.config import Config, load_config
from aiogram.fsm.storage.memory import MemoryStorage
# from app.midlewares import ShadowBanMiddleware
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
comands_data = {"/help": "Справка по работе бота", 
                "/cancel": "Закончить игру",
                "/stat": "Узнать количество побед",
                "/gamer": "Узнать рейтинг игроков",
                "/rate": "Зделать ставку",
                "/rank": "Класификация рангов",
                "/exchange": "Обмен"}
                
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [BotCommand(command=command, description=description) for command, description in comands_data.items()]
    await bot.set_my_commands(main_menu_commands)

async def main():
    await async_main()
    config: Config = load_config()
    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token)
    await bot.delete_webhook(drop_pending_updates=True)
    dp = Dispatcher(storage=storage)
    dp.include_routers(story_handlers.router,exchange_handlers.router, rate_handlers.router, handlers.router)
    # dp.update.middleware(ShadowBanMiddleware())
    # await set_main_menu(bot=bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот выключен")
    