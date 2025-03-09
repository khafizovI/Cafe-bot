from aiogram import Bot, Dispatcher, types, F
from aiogram.types import CallbackQuery, BotCommand, Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from buttons import main_menu
from database import init_db, get_all_users, add_user
import admin
import logging
import asyncio

TOKEN = "7805076022:AAEXbzgm7uE096iL0pQg8OQlovZaBWNdrFg"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(admin.router)

user_languages = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    await add_user(user_id, full_name)
    await message.answer(f"Xush kelibsiz, {full_name}! Kerakli bo'limni tanlang:", reply_markup=main_menu())

@dp.message(Command("id"))
async def get_id(message: types.Message):
    await message.answer(f"🆔 Sizning ID: {message.from_user.id}")

@dp.callback_query(F.data == "admin_add_product")
async def admin_add_product(callback_query: CallbackQuery, state: FSMContext):
    await admin.product_picture(callback_query.message, state)
    await callback_query.answer()

@dp.message(F.text == "📍 Bizning manzil")
async def send_location(message: Message):
    latitude, longitude = 41.340709, 69.268608
    await message.answer("📍 Bizning filial manzili:")
    await message.answer_location(latitude=latitude, longitude=longitude)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
    ]
    await bot.set_my_commands(commands)

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    users = await get_all_users()
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())