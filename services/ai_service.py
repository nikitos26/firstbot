import os
import uuid
import aiohttp
import asyncio
from datetime import datetime
from typing import Dict, Any

from config import Config

class AIService:
    """Сервис для работы с AI API"""
    
    def __init__(self):
        self.api_key = Config.KANDINSKY_API_KEY
        self.api_secret = getattr(Config, 'KANDINSKY_API_SECRET', None)
        self.api_url = Config.KANDINSKY_API_URL
        self.timeout = aiohttp.ClientTimeout(total=300)  # 5 минут
    
    async def generate_image(self, prompt: str) -> Dict[str, Any]:
        """Генерация изображения по текстовому описанию"""
        try:
            # Пробуем использовать Kandinsky API
            if self.api_key and self.api_secret:
                result = await self._call_kandinsky_api(prompt)
                if result['success']:
                    return result
                # Если API не сработал, добавим причину в примечание
                kandinsky_error_note = f"Kandinsky error: {result.get('error', 'unknown error')}"

            # Фолбэк: публичный Pollinations (без ключей)
            pollinations = await self._call_pollinations_api(prompt)
            if pollinations and os.path.exists(pollinations):
                return {
                    'success': True,
                    'image_path': pollinations,
                    'prompt': prompt,
                    'note': 'Сгенерировано через Pollinations (временный провайдер)'
                }
            
            # Если API недоступен, создаем заглушку
            result_path = await self._create_placeholder_image(prompt, "generated")
            
            return {
                'success': True,
                'image_path': result_path,
                'prompt': prompt,
                'note': 'Использована заглушка (API недоступен или ошибка). ' + (kandinsky_error_note if 'kandinsky_error_note' in locals() else 'Проверьте ключи и доступность API')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def edit_image(self, image_path: str, edit_prompt: str) -> Dict[str, Any]:
        """Редактирование изображения"""
        try:
            # Проверяем существование файла
            if not os.path.exists(image_path):
                return {
                    'success': False,
                    'error': 'Исходное изображение не найдено'
                }
            
            # Пока что возвращаем заглушку
            # В реальной реализации здесь будет вызов API
            await asyncio.sleep(3)  # Имитация обработки
            
            # Создаем заглушку отредактированного изображения
            result_path = await self._create_placeholder_image(edit_prompt, "edited")
            
            return {
                'success': True,
                'image_path': result_path,
                'edit_prompt': edit_prompt
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _create_placeholder_image(self, prompt: str, image_type: str) -> str:
        """Создание заглушки изображения (временно)"""
        try:
            # Создаем уникальное имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{image_type}_{timestamp}_{unique_id}.jpg"
            
            # Полный путь к файлу
            file_path = os.path.join(Config.OUTPUT_DIR, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Создаем простое изображение-заглушку
            from PIL import Image, ImageDraw, ImageFont
            
            # Создаем изображение 512x512
            img = Image.new('RGB', (512, 512), color='lightblue')
            draw = ImageDraw.Draw(img)
            
            # Добавляем текст
            try:
                # Пытаемся использовать системный шрифт
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
            except:
                # Если не получается, используем стандартный
                font = ImageFont.load_default()
            
            # Разбиваем текст на строки
            words = prompt.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + word) < 30:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
            
            # Рисуем текст
            y_position = 200
            for line in lines[:5]:  # Максимум 5 строк
                draw.text((50, y_position), line, fill='black', font=font)
                y_position += 30
            
            # Добавляем подпись
            draw.text((50, 450), f"AI Generated - {image_type}", fill='gray', font=font)
            
            # Сохраняем изображение
            img.save(file_path, 'JPEG')
            
            return file_path
            
        except Exception as e:
            print(f"Ошибка создания заглушки: {e}")
            # Возвращаем путь к дефолтному изображению
            return os.path.join(Config.OUTPUT_DIR, "default.jpg")
    
    async def _call_kandinsky_api(self, prompt: str, image_path: str = None) -> Dict[str, Any]:
        """Вызов API Kandinsky"""
        try:
            import aiohttp
            import json
            
            # Получаем модель
            model_id = await self._get_kandinsky_model_id()
            if not model_id:
                return { 'success': False, 'error': 'No model_id from FusionBrain' }

            # URL для генерации изображений
            url = f"{self.api_url}/key/api/v1/text2image/run"
            
            headers = {
                'X-Key': f'Key {self.api_key}',
                'X-Secret': f'Secret {self.api_secret}',
                # Content-Type не указываем вручную, aiohttp поставит multipart
            }
            
            params = {
                "type": "GENERATE",
                "numImages": 1,
                "width": 1024,
                "height": 1024,
                "generateParams": {
                    "query": prompt
                }
            }

            form = aiohttp.FormData()
            form.add_field('model_id', model_id)
            form.add_field('params', json.dumps(params), content_type='application/json')
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(url, headers=headers, data=form) as response:
                    if response.status == 200:
                        result = await response.json()
                        task_id = result.get('uuid')
                        
                        if task_id:
                            # Ждем завершения генерации
                            image_base64 = await self._wait_for_generation(task_id)
                            if image_base64:
                                # Сохраняем изображение из base64
                                local_path = await self._save_base64_image(image_base64, prompt)
                                return {
                                    'success': True,
                                    'image_path': local_path,
                                    'prompt': prompt
                                }
                            else:
                                return { 'success': False, 'error': 'Generation failed or timed out' }
                    else:
                        try:
                            text = await response.text()
                        except Exception:
                            text = ''
                        return {
                            'success': False,
                            'error': f'API error: {response.status} {text[:300]}'
                        }
                    
        except Exception as e:
            return {
                'success': False,
                'error': f'Kandinsky API error: {str(e)}'
            }
    
    async def _wait_for_generation(self, task_id: str) -> str:
        """Ожидание завершения генерации"""
        try:
            import aiohttp
            
            check_url = f"{self.api_url}/key/api/v1/text2image/status/{task_id}"
            headers = {
                'X-Key': f'Key {self.api_key}',
                'X-Secret': f'Secret {self.api_secret}'
            }
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                for _ in range(30):  # Максимум 30 попыток (5 минут)
                    async with session.get(check_url, headers=headers) as response:
                        if response.status == 200:
                            result = await response.json()
                            status = result.get('status')
                            
                            if status == 'DONE':
                                images = result.get('images', [])
                                if images:
                                    # API возвращает список base64 строк
                                    return images[0]
                            elif status == 'FAIL':
                                return None
                            
                            await asyncio.sleep(10)  # Ждем 10 секунд
                        else:
                            # Вернем None, но это будет отловлено выше
                            return None
                            
            return None
            
        except Exception as e:
            print(f"Ошибка ожидания генерации: {e}")
            return None

    async def _get_kandinsky_model_id(self) -> str:
        """Получение model_id из FusionBrain с учетом разных форматов ответа"""
        try:
            import aiohttp
            url = f"{self.api_url}/key/api/v1/models"
            headers = {
                'X-Key': f'Key {self.api_key}',
                'X-Secret': f'Secret {self.api_secret}',
                'Accept': 'application/json'
            }
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        try:
                            txt = await response.text()
                        except Exception:
                            txt = ''
                        print(f"FusionBrain /models error: {response.status} {txt[:300]}")
                        return None
                    data = await response.json()
                    # Приводим к списку моделей
                    models = []
                    if isinstance(data, list):
                        models = data
                    elif isinstance(data, dict):
                        # Популярные варианты ключей
                        for key in ('result', 'models', 'items', 'data'):
                            if isinstance(data.get(key), list):
                                models = data.get(key)
                                break
                    # Перебираем модели
                    for m in models:
                        name = str(m.get('name', '')).lower()
                        mid = str(m.get('id', ''))
                        mtype = str(m.get('type', '')).upper()
                        if 'kandinsky' in name or 'kandinsky' in mid or mtype in ('TEXT2IMAGE', 'TEXT_TO_IMAGE'):
                            return mid
                    # Если ничего не нашли, берем первую доступную
                    if models:
                        return str(models[0].get('id'))
        except Exception as e:
            print(f"Ошибка получения model_id: {e}")
        return None
    
    async def _save_base64_image(self, image_base64: str, prompt: str) -> str:
        """Сохранение изображения из base64"""
        try:
            import base64
            from datetime import datetime
            import uuid
            
            # Декодируем base64 и сохраняем
            decoded_data = base64.b64decode(image_base64)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"kandinsky_{timestamp}_{unique_id}.jpg"
            file_path = os.path.join(Config.OUTPUT_DIR, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(decoded_data)
            return file_path
            
        except Exception as e:
            print(f"Ошибка сохранения изображения: {e}")
            return None

    async def _call_pollinations_api(self, prompt: str) -> str:
        """Простой фолбэк-провайдер без ключей: Pollinations.ai"""
        try:
            import aiohttp
            import urllib.parse
            safe_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{safe_prompt}?nologo=true&width=1024&height=1024"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"pollinations_{timestamp}_{unique_id}.jpg"
            file_path = os.path.join(Config.OUTPUT_DIR, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        return file_path
        except Exception as e:
            print(f"Pollinations error: {e}")
        return None
    
    async def _call_shedevrum_api(self, prompt: str, image_path: str = None) -> Dict[str, Any]:
        """Вызов API Шедеврум (будет реализовано позже)"""
        # TODO: Реализовать реальный вызов API
        pass
