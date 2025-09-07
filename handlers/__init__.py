import sys
import os

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Dispatcher
from .basic import register_basic_handlers
from .image_generation import register_image_handlers
from .file_processing import register_file_handlers

def register_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков"""
    register_basic_handlers(dp)
    register_image_handlers(dp)
    register_file_handlers(dp)
