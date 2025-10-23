import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

# === Настройки ===
BOT_TOKEN = "8013345611:AAFLtY-kRoE5xkMiXZ9uzvoUJukSE96voXg"  # вставь токен бота от BotFather
API_URL = "https://chatgpt5.org/api/text"

# === Создаем экземпляры бота и диспетчера ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# === Обработчик команды /start ===
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Я готов пообщаться с тобой! 🤖")

# === Основная функция общения с API ===
async def ask_chatgpt(message: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://chatgpt5.org",
        "Referer": "https://chatgpt5.org/chat",
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "message": message,
        "recaptcha_token": "0.lepnWyO5mUMJZ9hmgX8VbxckCdpA5fo-t7TNFtAUephMHkOEHFz4jwjzYck-UVjB2eTfpAPUbcEpqfR9LJVx1d2cOwFzPnJugEiEzNiS6gSP8bgTq9lXoC8BS19h21xsIukS7WDVxfE-h5U9Ws9_gU0bvu3hqV_-L8F2EMoGg-i_zAH_mpV7b9IsgzVSj-yo8hg7xCZZKkvMEzmEjt0YE-28JmzvRjjZE3TzgfdnRy35iwgNFYltnpsHApnAf3CxRz0Bn8dHVjOflDhsODt2GlXLHOlqaVNOGcs3zqTMn-cVDTVMVhNmNFpwhZrCuJCD3lPG2ZWpZKsgy5oXzlnib7LEx46m-G6ndobU7fmENFzif0rtz9aBjgUnkc3wg1F9lhkGMHRo3_Pg0ugzy_Kz6kHUxONZNkqp60WsjcfjNtzndldqi7ZsTmOPtq6H4EXXUTp_uT9A1iJSLS8BYtgYiX_AZJOgI-QII88eWvZN5uFcagOaxFw1tiIBGepniGDke1bJUqsLTimlIxgpi00NHeQDBHTMr_O0s5K1X1pHIwfYSAaG9c6Umk6xi-zDxfWUIadPfxaGepbsWg3UlDTK7RtJS2TE2PPx6cREJ0KAh03ZTEb3AlrciUm6vQxstKI5CyTnFpONNiWhsjJ1hPHCaK6ZIyOgX2c5iofDHwuN6hmTUX_ivEEjiba8wJXCNxw1vEEs6yMF-qGBxmx7DpVkwGihwD_fl7YMlkIIuLXMfFmkhbqTbOvdbpn_Bl7gx_NNRo3NdPUluYrEQ6NChhD1GzSKR27mEaW_OgUaVgnGP8Gkd_U-D9bBD9nLNiGhtEj5WULCRPFcXeu1Cpy6LnpdWgGA13pIHh1bQy9jwjpOti9WZ7yMu9umvI8nPFhraM1NqttBDC0gMK43_JomDl7oeGCGiktLQokgHiYNmeAkd84.FZvi3t_hxJwGUJrGvgDXxQ.c3924ff42c2a1b048b9bfc002653c0df8405750c97dcaa38565ed324eec12c3b",  # можно оставить пустым или подставить при необходимости
        "temperature": 1,
        "presence_penalty": 0,
        "top_p": 1,
        "frequency_penalty": 0
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=data) as resp:
            if resp.status != 200:
                return f"Ошибка запроса: {resp.status}"
            try:
                response_json = await resp.json()
                return response_json.get("message", "Не удалось получить ответ.")
            except Exception as e:
                return f"Ошибка парсинга ответа: {e}"

# === Обработчик всех остальных сообщений ===
@dp.message()
async def echo_handler(message: types.Message):
    user_text = message.text
    mess = await message.answer("⏳ Думаю над ответом...")
    
    reply = await ask_chatgpt(user_text)
    await bot.edit_message_text(chat_id=mess.chat.id,
        message_id=mess.message_id,
        text=f"{reply}"
    )

# === Запуск бота ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
