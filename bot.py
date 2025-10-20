import json
import logging
import os
import tempfile
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
import httpx
from dotenv import load_dotenv
from elevenlabs import save
from elevenlabs.client import ElevenLabs

# --- Загрузка переменных окружения ---
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
LANGUAGE = os.getenv("LANGUAGE")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")
if not ELEVENLABS_API_KEY:
    raise ValueError("❌ ELEVENLABS_API_KEY не найден в .env")

# --- Настройки ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = os.getenv("MODEL")

HISTORY_FILE = Path("stories.json")
if HISTORY_FILE.exists():
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        user_stories = json.load(f)
else:
    user_stories = {}

ASK_AGE, GENERATE_STORY = range(2)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- Озвучка через ElevenLabs ---
def text_to_speech(text: str) -> str:
    """Генерирует аудио через ElevenLabs (актуальный API v1+)."""
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    
    # Используем text_to_speech.convert вместо client.generate
    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Или "Rachel", "Antoni" и т.д.
        model_id="eleven_multilingual_v2",
        text=text,
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    )
    
    # Сохраняем аудио
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tmp_path = tmp.name
    save(audio, tmp_path)
    return tmp_path

# --- Обработчики бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🌟 Я волшебный сказочник. Напиши имя твоего ребёнка, и я создам для него персонализированную сказку — и расскажу её тёплым голосом!"
    )
    return ASK_AGE

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name.isalpha():
        await update.message.reply_text("Пожалуйста, введи настоящее имя (только буквы).")
        return ASK_AGE
    context.user_data["name"] = name.capitalize()
    await update.message.reply_text("Сколько лет ребёнку? (Напиши число от 3 до 10)")
    return GENERATE_STORY

async def get_age_and_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        age = int(update.message.text.strip())
        if not (3 <= age <= 10):
            raise ValueError
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи возраст от 3 до 10.")
        return GENERATE_STORY

    name = context.user_data["name"]
    context.user_data["age"] = age

    # Формируем промпт с разнообразием и полом через ИИ
    prompt = f"""
Создай персонализированную, короткую и поучительную сказку для ребенка по имени {name}, которому(которой) {age} лет.

**Главный герой:**
*   Имя: {name}
*   Его/ее главная черта: [Например: любознательность, доброта, смелость, немного застенчив(а)]
*   Что он/она любит: [Например: рисовать, динозавров, космос, животных]

**Сюжет сказки:**
*   **Тема и место действия:** *Выбери на свое усмотрение интересную, добрую и подходящую для возраста ребенка тему и место действия. Это может быть волшебный лес, далекая планета, город говорящих животных, подводное царство или мир оживших игрушек.*
*   **Основная идея/мораль:** Сказка должна в доброй и иносказательной форме научить тому, что [Например: важно делиться с друзьями, не нужно бояться просить о помощи, убирать за собой игрушки - это правильно].

**Строгие ограничения:**
*   История должна быть абсолютно безопасной: без насилия, жестокости, монстров и пугающих ситуаций.
*   Длина: не более 500 слов (примерно 5-7 минут чтения вслух).
*   В тексте не должно быть лишних символов кроме литературных.
*   Заверши сказку на позитивной и воодушевляющей ноте.
*   Весь рассказ должен быть на {LANGUAGE} языке.
"""

    await update.message.reply_text("✨ Придумываю сказку и готовлю голос... (10–20 секунд)")

    # Генерация текста через Ollama
    try:
        timeout = httpx.Timeout(180.0, read=180.0, write=180.0, connect=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7}
                }
            )
            response.raise_for_status()
            story = response.json()["response"].strip()
    except Exception as e:
        logging.error(f"Ошибка генерации: {e}", exc_info=True)
        await update.message.reply_text(f"Ошибка при создании сказки: {str(e)[:100]}")
        return ConversationHandler.END

    # Сохраняем историю
    user_id = str(update.effective_user.id)
    if user_id not in user_stories:
        user_stories[user_id] = []
    user_stories[user_id].append({"name": name, "age": age, "story": story})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(user_stories, f, ensure_ascii=False, indent=2)

    # Отправляем текст
    await update.message.reply_text(story)

    # Озвучка через ElevenLabs
    try:
        audio_path = text_to_speech(story)
        with open(audio_path, 'rb') as audio_file:
            await update.message.reply_voice(voice=audio_file)
        os.unlink(audio_path)
    except Exception as e:
        logging.error(f"Ошибка ElevenLabs: {e}", exc_info=True)
        await update.message.reply_text("🎙️ Не удалось озвучить, но сказка готова! Прочитай её сам.")

    await update.message.reply_text("Спокойной ночи! 🌙\n\nХочешь ещё сказку? Напиши /start")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("До новых встреч! 🌟")
    return ConversationHandler.END

# --- Запуск ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GENERATE_STORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age_and_generate)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    logging.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()