from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton , KeyboardButton , ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo

WEB3_SHOP_URL = url="https://67ca912e486bf0e5bcfc8960--grand-mooncake-0410cc.netlify.app/"
WEB3_CART_URL = url= "https://67c9da889901da17006a1c2d--storied-dodol-8af7e5.netlify.app/"

def get_admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Mahsulot qo‘shish"),KeyboardButton(text="🗑 Mahsulotlarni ochirish")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True
    )

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Menu", web_app=WebAppInfo(url=WEB3_SHOP_URL))],
            [KeyboardButton(text="✍️ Taklif va shikoyatlar"),KeyboardButton(text="🛒 Savatcha",web_app=WebAppInfo(url=WEB3_CART_URL))],
            [KeyboardButton(text="📍 Bizning manzil")]
        ],
        resize_keyboard=True
    )

def back_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Orqaga")]],
        resize_keyboard=True
    )


def language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="lang_uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        ]
    )
