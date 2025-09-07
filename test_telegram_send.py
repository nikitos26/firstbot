#!/usr/bin/env python3
"""
Тестовый скрипт для проверки отправки изображений в Telegram
"""

import sys
import os
import asyncio

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot
from aiogram.types import FSInputFile
from config import Config

async def test_send_image():
    """Тестируем отправку изображения"""
    print("📤 Тестирование отправки изображения в Telegram...")
    
    try:
        # Создаем бота
        bot = Bot(token=Config.BOT_TOKEN)
        
        # Проверяем наличие тестового изображения
        test_images = []
        if os.path.exists('outputs'):
            for file in os.listdir('outputs'):
                if file.endswith('.jpg'):
                    test_images.append(os.path.join('outputs', file))
        
        if not test_images:
            print("❌ Нет тестовых изображений в папке outputs/")
            return False
        
        # Берем первое изображение
        test_image = test_images[0]
        print(f"📁 Используем изображение: {test_image}")
        
        # Создаем FSInputFile
        photo = FSInputFile(test_image)
        
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"🤖 Бот: @{bot_info.username}")
        
        # Отправляем изображение самому себе (для тестирования)
        try:
            await bot.send_photo(
                chat_id=bot_info.id,
                photo=photo,
                caption="🎨 <b>Тестовое изображение</b>\n\nЭто тест отправки изображения ботом."
            )
            print("✅ Изображение успешно отправлено!")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка создания бота: {e}")
        return False
    
    finally:
        await bot.session.close()

async def main():
    """Основная функция"""
    print("🤖 Тестирование отправки изображений в Telegram")
    print("=" * 60)
    
    success = await test_send_image()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Тест прошел успешно! Бот может отправлять изображения.")
    else:
        print("❌ Тест не прошел. Проверьте настройки.")
    
    print("\n💡 Если тест прошел, попробуйте бота в Telegram!")

if __name__ == "__main__":
    asyncio.run(main())
