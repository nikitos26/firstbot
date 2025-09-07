#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы бота без реального токена
"""

import sys
import os

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_bot_components():
    """Тестируем компоненты бота"""
    print("🤖 Тестирование компонентов бота...\n")
    
    # Тест 1: Импорт основных модулей
    print("1️⃣ Тестируем импорты...")
    try:
        from config import Config
        print("   ✅ config.py")
        
        from utils.keyboards import get_main_keyboard, get_generation_keyboard
        print("   ✅ utils.keyboards")
        
        from utils.file_utils import save_uploaded_file, validate_file
        print("   ✅ utils.file_utils")
        
        from services.ai_service import AIService
        print("   ✅ services.ai_service")
        
        from handlers.basic import register_basic_handlers
        print("   ✅ handlers.basic")
        
        from handlers.image_generation import register_image_handlers
        print("   ✅ handlers.image_generation")
        
        from handlers.file_processing import register_file_handlers
        print("   ✅ handlers.file_processing")
        
    except Exception as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False
    
    # Тест 2: Создание клавиатур
    print("\n2️⃣ Тестируем клавиатуры...")
    try:
        main_kb = get_main_keyboard()
        gen_kb = get_generation_keyboard()
        print("   ✅ Клавиатуры создаются успешно")
    except Exception as e:
        print(f"   ❌ Ошибка клавиатур: {e}")
        return False
    
    # Тест 3: AI сервис
    print("\n3️⃣ Тестируем AI сервис...")
    try:
        ai_service = AIService()
        print("   ✅ AI сервис создается успешно")
    except Exception as e:
        print(f"   ❌ Ошибка AI сервиса: {e}")
        return False
    
    # Тест 4: Проверка конфигурации
    print("\n4️⃣ Тестируем конфигурацию...")
    try:
        from config import Config
        # Проверяем, что токен не установлен
        if Config.BOT_TOKEN == 'your_bot_token_here':
            print("   ✅ Токен бота не установлен (ожидаемо)")
        else:
            print("   ⚠️  Токен бота установлен")
        
        # Проверяем директории
        dirs = [Config.UPLOAD_DIR, Config.OUTPUT_DIR, 'logs']
        for dir_name in dirs:
            if os.path.exists(dir_name):
                print(f"   ✅ Директория {dir_name}/ существует")
            else:
                print(f"   ❌ Директория {dir_name}/ не найдена")
        
    except Exception as e:
        print(f"   ❌ Ошибка конфигурации: {e}")
        return False
    
    return True

def test_ai_generation():
    """Тестируем генерацию изображений"""
    print("\n5️⃣ Тестируем генерацию изображений...")
    try:
        import asyncio
        from services.ai_service import AIService
        
        async def test_generation():
            ai_service = AIService()
            result = await ai_service.generate_image("тестовое изображение")
            
            if result['success']:
                print("   ✅ Генерация изображения работает")
                if os.path.exists(result['image_path']):
                    print("   ✅ Изображение сохранено")
                    return True
                else:
                    print("   ❌ Изображение не найдено")
                    return False
            else:
                print(f"   ❌ Ошибка генерации: {result['error']}")
                return False
        
        return asyncio.run(test_generation())
        
    except Exception as e:
        print(f"   ❌ Ошибка тестирования генерации: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование AI Art Bot\n")
    
    # Тестируем компоненты
    components_ok = test_bot_components()
    
    # Тестируем генерацию
    generation_ok = test_ai_generation()
    
    print("\n" + "="*50)
    print("📊 Результаты тестирования:")
    print(f"   Компоненты бота: {'✅' if components_ok else '❌'}")
    print(f"   Генерация изображений: {'✅' if generation_ok else '❌'}")
    
    if components_ok and generation_ok:
        print("\n🎉 Все тесты пройдены! Бот готов к работе.")
        print("\n📋 Для запуска бота:")
        print("1. Получи токен бота у @BotFather")
        print("2. Замени 'your_bot_token_here' в файле .env на реальный токен")
        print("3. Запусти: python main.py")
    else:
        print("\n⚠️  Некоторые тесты не пройдены. Проверь ошибки выше.")
    
    return components_ok and generation_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
