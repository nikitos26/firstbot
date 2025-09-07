from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """Главная клавиатура бота"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎨 Генерировать изображение")],
            [KeyboardButton(text="✏️ Редактировать изображение")],
            [KeyboardButton(text="📖 Помощь"), KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_generation_keyboard():
    """Клавиатура для генерации изображений"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Сгенерировать еще", callback_data="generate_another")],
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_generated")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard

def get_edit_keyboard():
    """Клавиатура для редактирования изображений"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Изменить стиль", callback_data="change_style")],
            [InlineKeyboardButton(text="🖼️ Добавить объект", callback_data="add_object")],
            [InlineKeyboardButton(text="🎭 Применить фильтр", callback_data="apply_filter")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard

def get_style_keyboard():
    """Клавиатура выбора стилей"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Аниме", callback_data="style_anime")],
            [InlineKeyboardButton(text="🖼️ Реализм", callback_data="style_realistic")],
            [InlineKeyboardButton(text="🎭 Киберпанк", callback_data="style_cyberpunk")],
            [InlineKeyboardButton(text="🌅 Импрессионизм", callback_data="style_impressionism")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_edit")]
        ]
    )
    return keyboard
