#!/usr/bin/env python3
"""
Telegram Bot для генерации и редактирования изображений/видео с помощью AI
"""

import asyncio
import logging
import os
import sys

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import Config
from handlers import register_handlers
from utils.logger import setup_logger

async def main():
    """Основная функция запуска бота"""
    
    # Настраиваем логирование
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        # Проверяем конфигурацию
        Config.validate()
        logger.info("Конфигурация загружена успешно")
        
        # Создаем директории для файлов
        os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        
        # Создаем бота и диспетчер
        bot = Bot(
            token=Config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()
        
        # Регистрируем обработчики
        register_handlers(dp)
        
        logger.info("Бот запускается...")
        
        # Запускаем бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise
    finally:
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
