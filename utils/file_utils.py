import os
import uuid
from datetime import datetime
from aiogram.types import PhotoSize
from config import Config

async def save_uploaded_file(photo: PhotoSize, upload_dir: str) -> str:
    """Сохранение загруженного файла"""
    try:
        # Создаем уникальное имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.jpg"
        
        # Полный путь к файлу
        file_path = os.path.join(upload_dir, filename)
        
        # Скачиваем файл
        file = await photo.get_file()
        await file.download(file_path)
        
        return file_path
        
    except Exception as e:
        print(f"Ошибка сохранения файла: {e}")
        return None

def validate_file(file_path: str, file_type: str = "image") -> bool:
    """Проверка валидности файла"""
    try:
        if not os.path.exists(file_path):
            return False
        
        # Проверяем размер файла
        file_size = os.path.getsize(file_path)
        
        if file_type == "image" and file_size > Config.MAX_IMAGE_SIZE:
            return False
        elif file_type == "video" and file_size > Config.MAX_VIDEO_SIZE:
            return False
        
        # Проверяем расширение файла
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if file_type == "image" and ext not in Config.SUPPORTED_IMAGE_FORMATS:
            return False
        elif file_type == "video" and ext not in Config.SUPPORTED_VIDEO_FORMATS:
            return False
        
        return True
        
    except Exception as e:
        print(f"Ошибка валидации файла: {e}")
        return False

def cleanup_old_files(directory: str, max_age_hours: int = 24):
    """Очистка старых файлов"""
    try:
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    print(f"Удален старый файл: {filename}")
                    
    except Exception as e:
        print(f"Ошибка очистки файлов: {e}")

def get_file_info(file_path: str) -> dict:
    """Получение информации о файле"""
    try:
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        _, ext = os.path.splitext(file_path)
        
        return {
            'size': stat.st_size,
            'extension': ext.lower(),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime)
        }
        
    except Exception as e:
        print(f"Ошибка получения информации о файле: {e}")
        return None
