#!/usr/bin/env python3
"""
Скрипт для перезапуска бота
"""

import os
import subprocess
import time
import signal

def kill_all_python_processes():
    """Останавливаем все процессы Python"""
    print("🛑 Останавливаем все процессы Python...")
    
    try:
        # Находим все процессы Python
        result = subprocess.run(['pgrep', '-f', 'python'], capture_output=True, text=True)
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"   ✅ Остановлен процесс {pid}")
                    except:
                        try:
                            os.kill(int(pid), signal.SIGKILL)
                            print(f"   ✅ Принудительно остановлен процесс {pid}")
                        except:
                            pass
        
        time.sleep(3)
        print("✅ Все процессы остановлены")
        
    except Exception as e:
        print(f"❌ Ошибка остановки процессов: {e}")

def start_bot():
    """Запускаем бота"""
    print("🚀 Запускаем бота...")
    
    try:
        # Активируем виртуальное окружение и запускаем бота
        cmd = "source venv/bin/activate && python main.py"
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)
        print("✅ Бот запущен")
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

def check_bot_status():
    """Проверяем статус бота"""
    print("🔍 Проверяем статус бота...")
    
    try:
        result = subprocess.run(['pgrep', '-f', 'python main.py'], capture_output=True, text=True)
        if result.stdout:
            print("✅ Бот запущен и работает")
            return True
        else:
            print("❌ Бот не запущен")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки статуса: {e}")
        return False

def main():
    """Основная функция"""
    print("🤖 Перезапуск AI Art Bot")
    print("=" * 40)
    
    # Останавливаем все процессы
    kill_all_python_processes()
    
    # Запускаем бота
    start_bot()
    
    # Проверяем статус
    if check_bot_status():
        print("\n🎉 Бот успешно перезапущен!")
        print("📱 Теперь можешь тестировать бота в Telegram")
    else:
        print("\n❌ Не удалось запустить бота")
        print("💡 Попробуй запустить вручную: source venv/bin/activate && python main.py")

if __name__ == "__main__":
    main()
