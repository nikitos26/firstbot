#!/usr/bin/env python3
"""
Скрипт для полной очистки и запуска бота
"""

import os
import subprocess
import time
import signal

def kill_all_processes():
    """Останавливаем все процессы"""
    print("🛑 Останавливаем все процессы...")
    
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
        
        time.sleep(5)
        print("✅ Все процессы остановлены")
        
    except Exception as e:
        print(f"❌ Ошибка остановки процессов: {e}")

def start_bot():
    """Запускаем бота"""
    print("🚀 Запускаем бота...")
    
    try:
        # Активируем виртуальное окружение и запускаем бота
        cmd = "source venv/bin/activate && python main.py"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)
        print("✅ Бот запущен")
        return process
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        return None

def main():
    """Основная функция"""
    print("🤖 Полная очистка и запуск AI Art Bot")
    print("=" * 50)
    
    # Останавливаем все процессы
    kill_all_processes()
    
    # Запускаем бота
    process = start_bot()
    
    if process:
        print("\n🎉 Бот успешно запущен!")
        print("📱 Теперь можешь тестировать бота в Telegram")
        print("🛑 Для остановки нажми Ctrl+C")
        
        try:
            # Ждем завершения
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Останавливаем бота...")
            process.terminate()
            print("✅ Бот остановлен")
    else:
        print("\n❌ Не удалось запустить бота")

if __name__ == "__main__":
    main()
