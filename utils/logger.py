import logging
import os
from datetime import datetime
from config import Config

def setup_logger():
    """Настройка системы логирования"""
    
    # Создаем директорию для логов
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Настраиваем формат логов
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Настраиваем уровень логирования
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    
    # Настраиваем файловый логгер
    log_filename = f"{log_dir}/bot_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Настраиваем консольный логгер
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Настраиваем логгер для aiogram
    aiogram_logger = logging.getLogger('aiogram')
    aiogram_logger.setLevel(logging.WARNING)  # Уменьшаем количество логов от aiogram
