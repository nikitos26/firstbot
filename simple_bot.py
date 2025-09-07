#!/usr/bin/env python3
"""
Простой тестовый бот для проверки отправки изображений
"""

import sys
import os
import asyncio

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from config import Config

# Создаем бота и диспетчер
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Команда /start"""
    await message.answer(
        "🎨 <b>AI Art Bot - Тестовая версия</b>\n\n"
        "Отправь мне текстовое описание изображения, и я сгенерирую его!"
    )

@dp.message(F.text)
async def handle_text(message: Message):
    """Обработка текстовых сообщений"""
    try:
        # Создаем простое изображение-заглушку
        from services.ai_service import AIService
        ai_service = AIService()
        
        # Генерируем изображение
        result = await ai_service.generate_image(message.text)
        
        if result['success']:
            # Отправляем изображение
            photo = FSInputFile(result['image_path'])
            caption = f"🎨 <b>Готово!</b>\n\n<i>Запрос:</i> {message.text}"
            if 'note' in result:
                caption += f"\n\n<i>{result['note']}</i>"
            
            await message.answer_photo(
                photo=photo,
                caption=caption
            )
        else:
            await message.answer(f"❌ Ошибка: {result['error']}")
            
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка: {str(e)}")

async def main():
    """Основная функция"""
    print("🤖 Запуск простого тестового бота...")
    print(f"📱 Бот: @{Config.BOT_TOKEN.split(':')[0]}")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
