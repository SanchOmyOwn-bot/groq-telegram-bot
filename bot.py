import os
import requests
from aiogram import Bot, Dispatcher, executor, types

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-70b-8192"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    return result["choices"][0]["message"]["content"]

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Hello! I am your Groq‑powered AI assistant. Send me a message!")

@dp.message_handler()
async def handle_message(message: types.Message):
    await message.chat.do("typing")
    reply = ask_groq(message.text)
    await message.answer(reply)

if __name__ == "__main__":
    executor.start_polling(dp)