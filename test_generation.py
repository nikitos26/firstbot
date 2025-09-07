#!/usr/bin/env python3
"""
Тестовый скрипт для проверки генерации изображений
"""

import sys
import os
import asyncio

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService

async def test_generation():
    """Тестируем генерацию изображений"""
    print("🎨 Тестирование генерации изображений...")
    
    ai_service = AIService()
    
    # Тестовые промпты
    test_prompts = [
        "Кот в космосе",
        "Портрет девушки в стиле аниме",
        "Футуристический город"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Тестируем: '{prompt}'")
        
        try:
            result = await ai_service.generate_image(prompt)
            
            if result['success']:
                print(f"   ✅ Успешно!")
                print(f"   📁 Файл: {result['image_path']}")
                if 'note' in result:
                    print(f"   ℹ️  {result['note']}")
                
                # Проверяем, что файл существует
                if os.path.exists(result['image_path']):
                    file_size = os.path.getsize(result['image_path'])
                    print(f"   📊 Размер: {file_size} байт")
                else:
                    print(f"   ❌ Файл не найден!")
            else:
                print(f"   ❌ Ошибка: {result['error']}")
                
        except Exception as e:
            print(f"   ❌ Исключение: {e}")

async def main():
    """Основная функция"""
    print("🤖 Тестирование AI Art Bot - Генерация изображений")
    print("=" * 60)
    
    await test_generation()
    
    print("\n" + "=" * 60)
    print("🎉 Тестирование завершено!")
    print("\n💡 Если все работает, бот готов к использованию в Telegram!")

if __name__ == "__main__":
    asyncio.run(main())
