#!/usr/bin/env python3
"""
Финальная версия бота с исправлениями
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
        "🎨 <b>AI Art Bot</b>\n\n"
        "Отправь мне текстовое описание изображения, и я сгенерирую его!\n\n"
        "Примеры:\n"
        "• Кот в космосе\n"
        "• Портрет девушки в стиле аниме\n"
        "• Футуристический город"
    )

@dp.message(F.text)
async def handle_text(message: Message):
    """Обработка текстовых сообщений"""
    try:
        # Проверяем, не является ли это командой
        if message.text.startswith('/'):
            return
        
        # Отправляем сообщение о начале обработки
        processing_msg = await message.answer(
            "🎨 <b>Генерирую изображение...</b>\n\n"
            f"<i>Запрос:</i> {message.text}\n"
            "⏳ Это может занять несколько секунд..."
        )
        
        # Создаем изображение
        from services.ai_service import AIService
        ai_service = AIService()
        
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
            
            # Удаляем сообщение о обработке
            await processing_msg.delete()
        else:
            await message.answer(f"❌ Ошибка генерации: {result['error']}")
            await processing_msg.delete()
            
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка: {str(e)}")
        print(f"Ошибка: {e}")

async def main():
    """Основная функция"""
    print("🤖 Запуск AI Art Bot...")
    
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"📱 Бот: @{bot_info.username}")
        print("✅ Бот запущен и готов к работе!")
        
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
