from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.ai_service import AIService
from utils.keyboards import get_generation_keyboard

class GenerationStates(StatesGroup):
    waiting_for_prompt = State()
    processing = State()

async def handle_text_generation(message: Message, state: FSMContext):
    """Обработка текстовых запросов для генерации изображений"""
    
    # Проверяем, не является ли это командой
    if message.text.startswith('/'):
        return
    
    # Проверяем длину промпта
    if len(message.text) < 3:
        await message.answer("❌ Описание слишком короткое. Попробуйте более подробное описание.")
        return
    
    if len(message.text) > 500:
        await message.answer("❌ Описание слишком длинное. Максимум 500 символов.")
        return
    
    # Отправляем сообщение о начале обработки
    processing_msg = await message.answer(
        "🎨 <b>Генерирую изображение...</b>\n\n"
        f"<i>Запрос:</i> {message.text}\n"
        "⏳ Это может занять несколько минут..."
    )
    
    try:
        # Генерируем изображение
        ai_service = AIService()
        result = await ai_service.generate_image(message.text)
        
        if result['success']:
            # Отправляем результат
            await message.answer_photo(
                photo=result['image_path'],
                caption=f"🎨 <b>Готово!</b>\n\n<i>Запрос:</i> {message.text}",
                reply_markup=get_generation_keyboard()
            )
            
            # Удаляем сообщение о обработке
            await processing_msg.delete()
            
        else:
            await message.answer(
                f"❌ <b>Ошибка генерации:</b>\n{result['error']}\n\n"
                "Попробуйте изменить описание или повторить позже."
            )
            await processing_msg.delete()
            
    except Exception as e:
        await message.answer(
            "❌ <b>Произошла ошибка при генерации изображения.</b>\n\n"
            "Попробуйте еще раз или обратитесь к администратору."
        )
        await processing_msg.delete()
        print(f"Ошибка генерации: {e}")

async def handle_generation_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка callback'ов для генерации"""
    
    if callback.data == "generate_another":
        await callback.message.answer(
            "🎨 <b>Генерация нового изображения</b>\n\n"
            "Отправьте новое описание желаемого изображения."
        )
        await state.set_state(GenerationStates.waiting_for_prompt)
    
    elif callback.data == "edit_generated":
        await callback.message.answer(
            "✏️ <b>Редактирование изображения</b>\n\n"
            "Отправьте описание желаемых изменений."
        )
        # Здесь можно добавить логику для редактирования
    
    elif callback.data == "back_to_main":
        await callback.message.answer(
            "🏠 <b>Главное меню</b>\n\n"
            "Выберите действие:",
            reply_markup=get_main_keyboard()
        )
    
    await callback.answer()

def register_image_handlers(dp: Dispatcher):
    """Регистрация обработчиков для генерации изображений"""
    dp.message.register(handle_text_generation, F.text)
    dp.callback_query.register(handle_generation_callback, F.data.startswith("generate_"))
