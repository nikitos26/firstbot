#!/usr/bin/env python3
"""
Простой тестовый бот для проверки работы
"""

import asyncio
import logging
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from config import Config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем бота и диспетчер
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer("🎨 <b>AI Art Bot</b>\n\nОтправь мне текстовое описание изображения!")

@dp.message(F.text)
async def handle_text(message: Message):
    """Обработчик текстовых сообщений"""
    if message.text.startswith('/'):
        return
    
    try:
        # Отправляем сообщение о начале генерации
        processing_msg = await message.answer("🎨 <b>Генерирую изображение...</b>")
        
        # Импортируем AI сервис
        from services.ai_service import AIService
        ai_service = AIService()
        
        # Генерируем изображение
        result = await ai_service.generate_image(message.text)
        
        if result['success']:
            # Отправляем изображение
            from aiogram.types import FSInputFile
            photo = FSInputFile(result['image_path'])
            caption = f"🎨 <b>Готово!</b>\n\n<i>Запрос:</i> {message.text}"
            if 'note' in result:
                caption += f"\n\n<i>{result['note']}</i>"
            
            await message.answer_photo(photo=photo, caption=caption)
            await processing_msg.delete()
        else:
            await message.answer(f"❌ Ошибка: {result['error']}")
            await processing_msg.delete()
            
    except Exception as e:
        logger.error(f"Ошибка при генерации: {e}")
        await message.answer(f"❌ Произошла ошибка: {str(e)}")

async def main():
    """Основная функция"""
    logger.info("🤖 Запуск простого тестового бота...")
    
    try:
        # Проверяем конфигурацию
        Config.validate()
        logger.info("✅ Конфигурация загружена")
        
        # Получаем информацию о боте
        me = await bot.get_me()
        logger.info(f"📱 Бот: @{me.username} (ID: {me.id})")
        
        # Запускаем polling
        logger.info("🚀 Бот запущен и готов к работе!")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
