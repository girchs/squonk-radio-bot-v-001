
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)

# Init bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Sample songs
songs = [
    {"file": "songs/squonk1.mp3", "comment": "This Squonk anthem hits harder than the last rug pull."},
    {"file": "songs/squonk2.mp3", "comment": "Tears, beats, and squonks – all in one."},
    {"file": "songs/squonk3.mp3", "comment": "Legend says this tune made a Solana validator cry."}
]

# Inline keyboard
def get_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("▶️ Next", callback_data="next"),
        InlineKeyboardButton("🔁 Replay", callback_data="replay")
    )
    return keyboard

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("👋 Welcome to Squonk Radio! Use /play to cry and vibe.")

@dp.message_handler(commands=["play"])
async def play_cmd(message: types.Message):
    song = random.choice(songs)
    with open(song["file"], "rb") as audio:
        await message.reply_audio(audio, caption=song["comment"], reply_markup=get_keyboard())

@dp.callback_query_handler(lambda c: c.data in ["next", "replay"])
async def callback_play(call: types.CallbackQuery):
    song = random.choice(songs) if call.data == "next" else songs[0]
    with open(song["file"], "rb") as audio:
        await bot.send_audio(call.message.chat.id, audio, caption=song["comment"], reply_markup=get_keyboard())
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
