from aiogram import Router, types, F , Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message
from buttons import get_admin_menu , main_menu
from database import get_all_users
import logging
import json
import os


router = Router()

ADMIN_ID = [802978542,5499596449]

PRODUCTS_FILE = "web3_products.json"

class AdminStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_delete_id = State()
    waiting_for_feedback = State()

@router.message(Command("admin"))
async def admin(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer("🔹 Admin panelga xush kelibsiz!", reply_markup=get_admin_menu())
    else:
        await message.answer("⛔ Siz admin emassiz!")


@router.message(F.text == "➕ Mahsulot qo‘shish")
async def product_picture(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await message.answer("📸 Mahsulot rasmini yuboring:")
        await state.set_state(AdminStates.waiting_for_photo)
    else:
        await message.answer("⛔ Faqat admin mahsulot qo‘shishi mumkin!")


@router.message(AdminStates.waiting_for_photo, F.photo)
async def product_name(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)

    await message.answer("✍️ Mahsulot nomini kiriting:")
    await state.set_state(AdminStates.waiting_for_name)


@router.message(AdminStates.waiting_for_name, F.text)
async def product_price(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Mahsulot narxini kiriting (so‘mda):")
    await state.set_state(AdminStates.waiting_for_price)


@router.message(AdminStates.waiting_for_price, F.text)
async def save_product(message: types.Message, state: FSMContext):
    try:
        price = int(message.text.replace(".", "").replace(",", ""))
    except ValueError:
        return await message.answer("❌ Iltimos, faqat son kiriting!")

    data = await state.get_data()
    product_id = get_next_product_id()

    product = {
        "id": product_id,
        "image": data["photo"],
        "name": data["name"],
        "price": price
    }

    save_product_to_file(product)
    await state.clear()

    formatted_price = f"{price:,}".replace(",", ".")

    await message.answer(f"✅ Mahsulot muvaffaqiyatli qo'shildi!\n"
                         f"🆔 ID: {product_id}\n"
                         f"📌 Narx: {formatted_price} so'm\n"
                         f"📌 U Web3 do‘konda aks etadi.")


def get_next_product_id():
    if not os.path.exists(PRODUCTS_FILE):
        return 1

    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict) and "products" in data:
                products = data["products"]
            elif isinstance(data, list):
                products = data
            else:
                return 1
    except (json.JSONDecodeError, FileNotFoundError):
        return 1

    return max((p.get("id", 0) for p in products), default=0) + 1


def save_product_to_file(product):
    if not isinstance(product, dict):
        raise ValueError("Mahsulot ma'lumoti noto‘g‘ri formatda!")

    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict) and "products" in data:
                products = data["products"]
            elif isinstance(data, list):
                products = data
            else:
                products = []
    except (FileNotFoundError, json.JSONDecodeError):
        products = []

    product["id"] = get_next_product_id()
    products.append(product)

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
        json.dump({"products": products}, file, indent=4, ensure_ascii=False)

    return product

@router.message(F.text == "🗑 Mahsulotlarni ochirish")
async def delete_product_start(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await message.answer("🔢 O‘chirish uchun mahsulot ID sini kiriting:")
        await state.set_state(AdminStates.waiting_for_delete_id)
    else:
        await message.answer("⛔ Faqat admin mahsulotni o‘chira oladi!")

@router.message(AdminStates.waiting_for_delete_id, F.text)
async def delete_product(message: types.Message, state: FSMContext):
    try:
        product_id = int(message.text)
    except ValueError:
        return await message.answer("❌ Iltimos, to‘g‘ri ID kiriting!")

    if remove_product_from_file(product_id):
        await message.answer(f"✅ Mahsulot ID {product_id} muvaffaqiyatli o‘chirildi!")
    else:
        await message.answer("❌ Bunday ID li mahsulot topilmadi!")

    await state.clear()

def remove_product_from_file(product_id):
    if not os.path.exists(PRODUCTS_FILE):
        return False

    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, dict) and "products" in data and isinstance(data["products"], list):
                products = data["products"]
            elif isinstance(data, list):
                products = data
            else:
                return False  # Agar format noto‘g‘ri bo‘lsa

    except (json.JSONDecodeError, FileNotFoundError):
        return False

    new_products = [p for p in products if isinstance(p, dict) and p.get("id") != product_id]

    if len(new_products) == len(products):
        return False

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
        json.dump({"products": new_products}, file, indent=4, ensure_ascii=False)

    return True

@router.message(F.text == "✍️ Taklif va shikoyatlar")
async def start_feedback(message: types.Message, state: FSMContext):
    await message.answer("📩 Taklif yoki shikoyatingizni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdminStates.waiting_for_feedback)

@router.message(AdminStates.waiting_for_feedback, F.text)
async def send_feedback_to_admins(message: types.Message, state: FSMContext):
    text = f"📩 Yangi taklif/shikoyat!\n👤 Kimdan: {message.from_user.full_name} (@{message.from_user.username})\n\n💬 Xabar:\n{message.text}"

    for admin in ADMIN_ID:
        try:
            await message.bot.send_message(admin, text)
        except Exception as e:
            print(f"Xatolik: {e}")

    await message.answer("✅ Taklif yoki shikoyatingiz yuborildi! Rahmat. 🙏", reply_markup=main_menu())
    await state.clear()


@router.channel_post()
async def forward_channel_post(message: Message, bot: Bot):
    CHANNEL_ID = -1002473038791

    if message.chat.id != CHANNEL_ID:
        return

    users = await get_all_users()

    try:
        if message.photo:
            photo_id = message.photo[-1].file_id
            caption = message.caption if message.caption else ""
            for user_id in users:
                await bot.send_photo(user_id, photo=photo_id, caption=caption)

        elif message.video:
            video_id = message.video.file_id
            caption = message.caption if message.caption else ""
            for user_id in users:
                await bot.send_video(user_id, video=video_id, caption=caption)

        elif message.text:
            text = message.text
            for user_id in users:
                await bot.send_message(user_id, text)

    except Exception as e:
        logging.error(f"Xatolik: {e}")


@router.message(F.text == "🔙 Orqaga")
async def go_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔙 Menu ga qaytdingiz!", reply_markup=main_menu())