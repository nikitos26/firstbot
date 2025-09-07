from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from utils.keyboards import get_main_keyboard

async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()
    
    welcome_text = """
🎨 <b>Добро пожаловать в AI Art Bot!</b>

Я помогу вам:
• 🖼️ Генерировать изображения по текстовому описанию
• ✏️ Редактировать ваши изображения
• 🎬 Обрабатывать видео

<b>Доступные команды:</b>
/start - Начать работу
/help - Помощь
/generate - Генерация изображения
/edit - Редактирование изображения

Просто отправьте мне текстовое описание картинки или загрузите изображение для редактирования!
    """
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = """
📖 <b>Справка по использованию бота</b>

<b>Генерация изображений:</b>
• Отправьте текстовое описание желаемого изображения
• Или используйте команду /generate

<b>Редактирование изображений:</b>
• Загрузите изображение в чат
• Добавьте описание желаемых изменений
• Или используйте команду /edit

<b>Поддерживаемые форматы:</b>
• Изображения: JPG, PNG, WebP
• Видео: MP4, AVI, MOV

<b>Ограничения:</b>
• Размер изображения: до 10 МБ
• Размер видео: до 100 МБ

<b>Примеры запросов:</b>
• "Кот в космосе"
• "Портрет девушки в стиле аниме"
• "Футуристический город"
    """
    
    await message.answer(help_text)

async def cmd_generate(message: Message, state: FSMContext):
    """Обработчик команды /generate"""
    await message.answer(
        "🎨 <b>Генерация изображения</b>\n\n"
        "Отправьте текстовое описание желаемого изображения.\n"
        "Например: 'Кот в космосе' или 'Портрет девушки в стиле аниме'"
    )
    # Здесь можно добавить состояние для ожидания промпта

async def cmd_edit(message: Message, state: FSMContext):
    """Обработчик команды /edit"""
    await message.answer(
        "✏️ <b>Редактирование изображения</b>\n\n"
        "Загрузите изображение, которое хотите отредактировать, "
        "и добавьте описание желаемых изменений."
    )
    # Здесь можно добавить состояние для ожидания изображения

def register_basic_handlers(dp: Dispatcher):
    """Регистрация базовых обработчиков"""
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_generate, Command("generate"))
    dp.message.register(cmd_edit, Command("edit"))
