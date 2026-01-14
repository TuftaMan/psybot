import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import client
from app.database.models import init_models
from app.admin.handlers import admin


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s- %(message)s')

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_BOT_KEY'))
    dp = Dispatcher()
    dp.include_routers(client, admin)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await init_models()
    logging.info('Bot started up...')


async def shutdown(dispatcher: Dispatcher):
    logging.info('bot shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped')
        os._exit(0) #убрать на деплое