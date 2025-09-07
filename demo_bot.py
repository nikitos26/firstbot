#!/usr/bin/env python3
"""
Демонстрационный скрипт для показа работы бота
"""

import sys
import os
import asyncio

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService
from utils.keyboards import get_main_keyboard, get_generation_keyboard, get_edit_keyboard

async def demo_ai_generation():
    """Демонстрация генерации изображений"""
    print("🎨 Демонстрация генерации изображений...")
    
    ai_service = AIService()
    
    # Тестовые промпты
    prompts = [
        "Кот в космосе",
        "Портрет девушки в стиле аниме",
        "Футуристический город"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{i}. Генерируем: '{prompt}'")
        
        result = await ai_service.generate_image(prompt)
        
        if result['success']:
            print(f"   ✅ Успешно! Изображение сохранено: {result['image_path']}")
        else:
            print(f"   ❌ Ошибка: {result['error']}")

def demo_keyboards():
    """Демонстрация клавиатур"""
    print("\n⌨️  Демонстрация клавиатур...")
    
    try:
        main_kb = get_main_keyboard()
        print("   ✅ Главная клавиатура создана")
        
        gen_kb = get_generation_keyboard()
        print("   ✅ Клавиатура генерации создана")
        
        edit_kb = get_edit_keyboard()
        print("   ✅ Клавиатура редактирования создана")
        
    except Exception as e:
        print(f"   ❌ Ошибка создания клавиатур: {e}")

def demo_file_operations():
    """Демонстрация работы с файлами"""
    print("\n📁 Демонстрация работы с файлами...")
    
    # Проверяем директории
    dirs = ['uploads', 'outputs', 'logs']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            files = os.listdir(dir_name)
            print(f"   ✅ {dir_name}/: {len(files)} файлов")
        else:
            print(f"   ❌ {dir_name}/: не найдена")

def show_bot_info():
    """Показываем информацию о боте"""
    print("🤖 AI Art Bot - Демонстрация возможностей")
    print("=" * 50)
    
    print("\n📋 Функциональность:")
    print("   • 🎨 Генерация изображений по тексту")
    print("   • ✏️  Редактирование загруженных изображений")
    print("   • 🎬 Обработка видео (в разработке)")
    print("   • ⌨️  Удобные клавиатуры и интерфейс")
    print("   • 📝 Логирование и обработка ошибок")
    
    print("\n🔧 Технологии:")
    print("   • Python 3.9+ с aiogram 3.4.1")
    print("   • Асинхронная архитектура")
    print("   • Система состояний (FSM)")
    print("   • Поддержка различных форматов файлов")
    
    print("\n🌍 AI сервисы (планируется):")
    print("   • Kandinsky (Сбер) - российский сервис")
    print("   • Шедеврум (Яндекс) - российский сервис")
    print("   • Leonardo.AI - международный сервис")

async def main():
    """Основная функция демонстрации"""
    show_bot_info()
    
    demo_keyboards()
    demo_file_operations()
    await demo_ai_generation()
    
    print("\n" + "=" * 50)
    print("🎉 Демонстрация завершена!")
    print("\n📋 Для запуска реального бота:")
    print("1. Получи токен у @BotFather в Telegram")
    print("2. Замени 'your_bot_token_here' в файле .env")
    print("3. Запусти: python main.py")
    print("\n💡 Бот готов к работе с реальными AI сервисами!")

if __name__ == "__main__":
    asyncio.run(main())
