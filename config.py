import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Config:
    """Конфигурация бота"""
    
    # Telegram Bot
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # AI Services
    KANDINSKY_API_KEY = os.getenv('KANDINSKY_API_KEY')
    KANDINSKY_API_SECRET = os.getenv('KANDINSKY_API_SECRET')
    KANDINSKY_API_URL = os.getenv('KANDINSKY_API_URL', 'https://api-key.fusionbrain.ai')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # File paths
    UPLOAD_DIR = 'uploads'
    OUTPUT_DIR = 'outputs'
    
    # Supported formats
    SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov']
    
    # Max file sizes (in bytes)
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
    
    @classmethod
    def validate(cls):
        """Проверяем наличие обязательных переменных"""
        if not cls.BOT_TOKEN or cls.BOT_TOKEN == 'your_bot_token_here':
            raise ValueError("BOT_TOKEN не найден в переменных окружения. Добавьте токен в файл .env")
        return True
