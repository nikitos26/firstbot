import sys
import os

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.ai_service import AIService
from utils.file_utils import save_uploaded_file, validate_file
from utils.keyboards import get_edit_keyboard, get_style_keyboard, get_main_keyboard
from config import Config

class EditStates(StatesGroup):
    waiting_for_image = State()
    waiting_for_edit_prompt = State()
    processing = State()

async def handle_photo_upload(message: Message, state: FSMContext):
    """Обработка загруженных фотографий"""
    
    try:
        # Получаем файл с наилучшим качеством
        photo = message.photo[-1]
        
        # Проверяем размер файла
        if photo.file_size > Config.MAX_IMAGE_SIZE:
            await message.answer(
                f"❌ <b>Файл слишком большой!</b>\n\n"
                f"Максимальный размер: {Config.MAX_IMAGE_SIZE // (1024*1024)} МБ\n"
                f"Размер вашего файла: {photo.file_size // (1024*1024)} МБ"
            )
            return
        
        # Сохраняем файл
        file_path = await save_uploaded_file(photo, Config.UPLOAD_DIR)
        
        if file_path:
            # Сохраняем путь к файлу в состоянии
            await state.update_data(image_path=file_path)
            await state.set_state(EditStates.waiting_for_edit_prompt)
            
            await message.answer(
                "✅ <b>Изображение загружено!</b>\n\n"
                "Теперь отправьте описание желаемых изменений.\n"
                "Например: 'Сделай в стиле аниме' или 'Добавь кота'",
                reply_markup=get_edit_keyboard()
            )
        else:
            await message.answer("❌ Ошибка при сохранении изображения.")
            
    except Exception as e:
        await message.answer("❌ Произошла ошибка при обработке изображения.")
        print(f"Ошибка обработки фото: {e}")

async def handle_edit_prompt(message: Message, state: FSMContext):
    """Обработка промпта для редактирования"""
    
    data = await state.get_data()
    image_path = data.get('image_path')
    
    if not image_path:
        await message.answer("❌ Изображение не найдено. Загрузите изображение заново.")
        await state.clear()
        return
    
    # Проверяем длину промпта
    if len(message.text) < 3:
        await message.answer("❌ Описание изменений слишком короткое.")
        return
    
    # Отправляем сообщение о начале обработки
    processing_msg = await message.answer(
        "✏️ <b>Редактирую изображение...</b>\n\n"
        f"<i>Изменения:</i> {message.text}\n"
        "⏳ Это может занять несколько минут..."
    )
    
    try:
        # Редактируем изображение
        ai_service = AIService()
        result = await ai_service.edit_image(image_path, message.text)
        
        if result['success']:
            # Отправляем результат
            try:
                caption = f"✏️ <b>Готово!</b>\n\n<i>Изменения:</i> {message.text}"
                if 'note' in result:
                    caption += f"\n\n<i>{result['note']}</i>"
                
                # Отправляем изображение как файл
                from aiogram.types import FSInputFile
                photo = FSInputFile(result['image_path'])
                
                await message.answer_photo(
                    photo=photo,
                    caption=caption,
                    reply_markup=get_edit_keyboard()
                )
                
                # Удаляем сообщение о обработке
                await processing_msg.delete()
                
            except Exception as e:
                await message.answer(
                    f"❌ <b>Ошибка отправки изображения:</b>\n{str(e)}\n\n"
                    "Попробуйте еще раз."
                )
                await processing_msg.delete()
            
        else:
            await message.answer(
                f"❌ <b>Ошибка редактирования:</b>\n{result['error']}\n\n"
                "Попробуйте изменить описание или повторить позже."
            )
            await processing_msg.delete()
            
    except Exception as e:
        await message.answer(
            "❌ <b>Произошла ошибка при редактировании изображения.</b>\n\n"
            "Попробуйте еще раз или обратитесь к администратору."
        )
        await processing_msg.delete()
        print(f"Ошибка редактирования: {e}")
    
    finally:
        await state.clear()

async def handle_edit_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка callback'ов для редактирования"""
    
    if callback.data == "change_style":
        await callback.message.answer(
            "🎨 <b>Выберите стиль:</b>",
            reply_markup=get_style_keyboard()
        )
    
    elif callback.data.startswith("style_"):
        style = callback.data.replace("style_", "")
        await callback.message.answer(
            f"🎨 <b>Стиль выбран:</b> {style}\n\n"
            "Теперь отправьте описание желаемых изменений."
        )
        await state.set_state(EditStates.waiting_for_edit_prompt)
    
    elif callback.data == "back_to_edit":
        await callback.message.answer(
            "✏️ <b>Редактирование изображения</b>\n\n"
            "Выберите тип изменений:",
            reply_markup=get_edit_keyboard()
        )
    
    elif callback.data == "back_to_main":
        await callback.message.answer(
            "🏠 <b>Главное меню</b>\n\n"
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
    
    await callback.answer()

def register_file_handlers(dp: Dispatcher):
    """Регистрация обработчиков для работы с файлами"""
    dp.message.register(handle_photo_upload, F.photo)
    dp.message.register(handle_edit_prompt, EditStates.waiting_for_edit_prompt)
    dp.callback_query.register(handle_edit_callback, F.data.startswith(("edit_", "style_", "back_to_")))
