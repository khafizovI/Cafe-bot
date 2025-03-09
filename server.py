from flask import Flask, jsonify, request
from flask_cors import CORS
from main import TOKEN as BOT_TOKEN
import json
import requests

app = Flask(__name__)
CORS(app)

JSON_FILE = "web3_products.json"

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id="


def load_products():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"products": []}


def save_products(data):
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_telegram_file_url(file_id):
    response = requests.get(TELEGRAM_API_URL + file_id).json()
    if response.get("ok"):
        file_path = response["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    return None


@app.route('/products', methods=['GET'])
def get_products():
    """Barcha mahsulotlarni qaytaradi, agar rasm ID bo'lsa, URL'ga aylantiradi."""
    data = load_products()

    for product in data["products"]:
        if not product["image"].startswith("http"):
            product["image"] = get_telegram_file_url(product["image"]) or product["image"]

    return jsonify(data)


@app.route('/add_product', methods=['POST'])
def add_product():
    """Yangi mahsulot qo‘shish"""
    new_product = request.json
    data = load_products()
    new_product["id"] = len(data["products"]) + 1

    # Agar rasm ID bo‘lsa, uni URL'ga aylantiramiz
    if not new_product["image"].startswith("http"):
        new_product["image"] = get_telegram_file_url(new_product["image"])

    data["products"].append(new_product)
    save_products(data)
    return jsonify({"message": "Mahsulot qo'shildi!"}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)
