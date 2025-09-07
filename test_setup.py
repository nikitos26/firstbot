#!/usr/bin/env python3
"""
Тестовый скрипт для проверки настройки проекта
"""

import sys
import os

def test_imports():
    """Тестируем импорты"""
    print("🔍 Тестируем импорты...")
    
    try:
        import aiogram
        print(f"✅ aiogram {aiogram.__version__}")
    except ImportError as e:
        print(f"❌ aiogram: {e}")
        return False
    
    try:
        import aiohttp
        print(f"✅ aiohttp {aiohttp.__version__}")
    except ImportError as e:
        print(f"❌ aiohttp: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✅ Pillow (PIL)")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print(f"✅ python-dotenv")
    except ImportError as e:
        print(f"❌ python-dotenv: {e}")
        return False
    
    return True

def test_config():
    """Тестируем конфигурацию"""
    print("\n🔧 Тестируем конфигурацию...")
    
    try:
        from config import Config
        print("✅ Конфигурация загружена")
        
        # Проверяем наличие .env файла
        if os.path.exists('.env'):
            print("✅ Файл .env найден")
        else:
            print("⚠️  Файл .env не найден")
        
        # Проверяем директории
        dirs = ['uploads', 'outputs', 'logs']
        for dir_name in dirs:
            if os.path.exists(dir_name):
                print(f"✅ Директория {dir_name}/ создана")
            else:
                print(f"❌ Директория {dir_name}/ не найдена")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_handlers():
    """Тестируем обработчики"""
    print("\n📝 Тестируем обработчики...")
    
    try:
        from handlers import register_handlers
        print("✅ Обработчики импортированы")
        
        from utils.keyboards import get_main_keyboard
        print("✅ Клавиатуры импортированы")
        
        from services.ai_service import AIService
        print("✅ AI сервис импортирован")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обработчиков: {e}")
        return False

def test_ai_service():
    """Тестируем AI сервис"""
    print("\n🤖 Тестируем AI сервис...")
    
    try:
        from services.ai_service import AIService
        ai_service = AIService()
        print("✅ AI сервис создан")
        
        # Тестируем создание заглушки
        import asyncio
        async def test_placeholder():
            result = await ai_service._create_placeholder_image("тест", "test")
            if os.path.exists(result):
                print("✅ Заглушка изображения создана")
                return True
            else:
                print("❌ Заглушка изображения не создана")
                return False
        
        return asyncio.run(test_placeholder())
        
    except Exception as e:
        print(f"❌ Ошибка AI сервиса: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование настройки AI Art Bot\n")
    
    tests = [
        test_imports,
        test_config,
        test_handlers,
        test_ai_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Проект готов к работе.")
        print("\n📋 Следующие шаги:")
        print("1. Получи токен бота у @BotFather в Telegram")
        print("2. Добавь токен в файл .env")
        print("3. Запусти бота: python main.py")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверь ошибки выше.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
