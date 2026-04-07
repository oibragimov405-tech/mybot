import telebot
from telebot import types
from datetime import datetime

CHANNEL = -1003705539547

TOKEN = "8301712601:AAEfCiJgIxCya2FR4gz2DbdD322Q419a3oY"
ADMIN_ID = 8360625353

import json
try:
   with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = []

users = [u for u in users if isinstance(u, dict)]

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['pay'])
def pay(message):
    bot.send_invoice(
        chat_id=message.chat.id,
        title="⭐ Stars sotib olish",
        description="Telegram Stars orqali to‘lov",
        payload="stars_payment",
        provider_token="",  # BO‘SH
        currency="XTR",     # ⭐
        prices=[types.LabeledPrice("100 Stars", 100)]
    )

@bot.message_handler(commands=['id'])
def get_id(message):
    chat = bot.get_chat("@nexoweivnews")
    print(chat.id)
    bot.send_message(message.chat.id, str(chat.id))

def check_subscribe(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def xizmatlar_menu():
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton("📱 Telegram", callback_data="tg"),
        InlineKeyboardButton("📸 Instagram", callback_data="insta")
    )
    markup.row(
        InlineKeyboardButton("🎵 TikTok", callback_data="tt"),
        InlineKeyboardButton("▶️ YouTube", callback_data="yt")
    )
    markup.row(
        InlineKeyboardButton("🔥 Bepul xizmat", callback_data="free")
    )
    markup.row(
        InlineKeyboardButton("⭐ Stars / Gift", callback_data="stars")
    )
    markup.row(
        InlineKeyboardButton("🔙 Orqaga", callback_data="back")
    )

    return markup
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "tg":
        bot.send_message(call.message.chat.id, "📱 Telegram xizmatlari")

    elif call.data == "insta":
        bot.send_message(call.message.chat.id, "📸 Instagram xizmatlari")

    elif call.data == "back":
        bot.send_message(call.message.chat.id, "🏠 Menu", reply_markup=main_menu())

# ================== START ==================
@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscribe(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(
            "📢 Kanalga obuna bo‘lish",
            url="https://t.me/nexoweivnews"
        )
        markup.add(btn)

        bot.send_message(
            message.chat.id,
            "❌ Avval kanalga obuna bo‘ling!",
            reply_markup=markup
        )
        return

    bot.send_message(message.chat.id, "Bot ishlayapti ✅")
    user_id = message.from_user.id

    if not any(isinstance(u, dict) and u.get('id') == user_id for u in users):
        user = {
    "id": user_id,
    "name": message.from_user.first_name,
    "username": message.from_user.username,
    "balance": 0,
    "spent": 0,
    "deposited": 0,
    "orders": 0,
    "numbers": 0,
    "referrals": 0,
    "stars": 0
}

        users.append(user)

        with open("users.json", "w") as f:
            json.dump(users, f)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("📞 Nomer olish", "🛍 Xizmatlar")
    markup.row("💳 Mening hisobim", "📦 Buyurtmalarim")
    markup.row("💰 Hisob to‘ldirish", "🚀 Kanalim")
    markup.row("📚 Qo‘llanma", "☎️ Qo‘llab-quvvatlash")

    if message.from_user.id == ADMIN_ID:
        markup.row("⚙️ Admin panel")
    else:
        markup.row("🤝 Hamkor bo‘lish")

    text = f"""
👋 Assalomu alaykum!

🤖 @{bot.get_me().username} - xizmatlar boti

📊 Xizmatlar:
👥 Obunachilar
📱 Virtual raqamlar
⭐ Telegram Stars

⚡ Tezkor • Qulay • Ishonchli

📚 Qo'llanma: /qollanma
"""

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "🛍 Xizmatlar")
def xizmatlar(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return

    bot.send_message(
        message.chat.id,
        "Tarmoqlardan birini tanlang:",
        reply_markup=xizmatlar_menu()
    )
@bot.message_handler(func=lambda m: m.text == "💰 Hisob to‘ldirish")
def deposit(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return

    text = """💎 Balansni to‘ldirish

➕ Balansga pul qo‘shish uchun to‘lov tizimini tanlang:

💳 Karta (Avtomatik)
O‘zingizga qulay ilovadan bot bergan kartaga bot ko‘rsatgan summani yuborasiz va avto tushadi.

⭐ Stars (Avtomatik)
Telegram stars orqali botga to‘lov qilishingiz mumkin

🔥 O‘zingizga qulay bo‘lgan to‘lov turini tanlang"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("💳 Karta (Avtomatik)")
    markup.row("⭐ Stars (Avtomatik)")
    markup.row("🧑‍💻 Admin orqali hisob to‘ldirish")
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, text, reply_markup=markup)
# ⭐ Stars tugma bosilganda
@bot.message_handler(func=lambda m: m.text == "⭐ Stars (Avtomatik)")
def stars_payment(message):
    bot.send_invoice(
        message.chat.id,              # chat_id
        "⭐ Stars sotib olish",        # title
        "Telegram Stars orqali to‘lov", # description
        "stars123",                   # ✅ payload (BU MAJBURIY!)
        "",                           # provider_token
        "XTR",                        # currency
        [types.LabeledPrice("100 Stars", 100)]
    )   
@bot.message_handler(func=lambda m: m.text == "🧑‍💻 Admin orqali hisob to‘ldirish")
def admin_contact(message):
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "✍️ Adminga yozish",
            url="https://t.me/smmgarand"
        )
    )

    bot.send_message(
        message.chat.id,
        "🧑‍💻 Admin orqali hisob to‘ldirish uchun pastdagi tugmani bosing:",
        reply_markup=markup
    )


# ===== QOLLAB QUVVATLASH =====
@bot.message_handler(func=lambda m: m.text == "☎️ Qo‘llab-quvvatlash")
def help_user(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return

    msg = bot.send_message(message.chat.id, "✍️ Xabaringizni yozing:")
    bot.register_next_step_handler(msg, send_to_admin)

# ================== ISHGA TUSHIRISH ==================
print("Bot ishlayapti...")
@bot.message_handler(func=lambda m: m.text == "📱 Telegram")
def telegram_menu(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("⭐ Premium", "🌟 Stars")
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, "📱 Telegram xizmatlari:", reply_markup=markup)


# ================== QO‘LLANMA ==================
@bot.message_handler(commands=['qollanma'])
@bot.message_handler(func=lambda m: m.text == "📚 Qo‘llanma")
def qollanma(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return
    text = """⚫ Botdan foydalanish yo‘riqnomasi:

🔄 Buyurtma bekor qilindimi?
Xavotir olmang! Agar buyurtma bekor qilinsa, mablag‘ avtomatik qaytariladi.

⏱ To‘lovni tasdiqlash vaqti:
To‘lovdan so‘ng 1–2 daqiqa kuting. Agar tushmasa, adminga yozing.

🚫 Mablag‘ni qaytarish:
Bot balansiga tushgan mablag‘ qaytarilmaydi.

✉️ Buyurtma savollari:
Muammo bo‘lsa, admin bilan bog‘laning.

🔔 Ketma-ket buyurtma:
Bir linkka bir vaqtning o‘zida bir nechta buyurtma bermang.

🎯 Referal tizimi:
Do‘stingiz shartlarni bajarmasa, bonus berilmaydi.

❗ Texnik yordam: @smmgarand
"""
    bot.send_message(message.chat.id, text)

# ================== HISOBIM ==================
@bot.message_handler(func=lambda m: m.text == "💳 Mening hisobim")
def kabinet(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return  

    user_id = message.from_user.id

    # userni topamiz
    user_data = next((u for u in users if u.get("id") == user_id), None)

    if not user_data:
        bot.send_message(message.chat.id, "❌ User topilmadi")
        return

    balance = user_data.get("balance", 0)
    spent = user_data.get("spent", 0)
    deposited = user_data.get("deposited", 0)

    vaqt = datetime.now().strftime("%H:%M")

    text = f"""🪪 Shaxsiy kabinet

┌ Ism: {message.from_user.first_name}
├ ID: {user_id}
└ Aloqa: mavjud emas

💰 Moliya:
├ Asosiy balans: {balance} so‘m
├ Sarflangan: {spent} so‘m
└ Kiritilgan: {deposited} so‘m

📊 Statistika:
├ Buyurtmalar: {user_data.get("orders", 0)} ta
├ Olingan raqamlar: {user_data.get("numbers", 0)} ta
├ Takliflar: {user_data.get("referrals", 0)} kishi
└ Telegram Stars: {user_data.get("stars", 0)} ⭐

⏰ Vaqt: {vaqt}
"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💸 Pul ishlash")
    markup.row("➡️ Pul o‘tkazish", "🔙 Orqaga")

    bot.send_message(message.chat.id, text, reply_markup=markup)


# ================== ORQAGA ==================
@bot.message_handler(func=lambda m: "Orqaga" in m.text)
def orqaga(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return   

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📱 Nomer olish", "🛍 Xizmatlar")
    markup.row("💳 Mening hisobim", "📦 Buyurtmalarim")
    markup.row("💰 Hisob to‘ldirish", "🚀 Kanalim")
    markup.row("📚 Qo‘llanma", "☎️ Qo‘llab-quvvatlash")

    if message.from_user.id == ADMIN_ID:
        markup.row("⚙️ Admin panel")
    else:
        markup.row("🤝 Hamkor bo‘lish")

    bot.send_message(message.chat.id, "🏠 Menu", reply_markup=markup)


# ================== YORDAM (ADMIN) ==================
@bot.message_handler(func=lambda m: m.text == "☎️ Yordam")
def yordam(message):
    if not check_subscribe(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!")
        return

    msg = bot.send_message(message.chat.id, "✍️ Xabaringizni yozing:")
    bot.register_next_step_handler(msg, send_to_admin)

def send_to_admin(message):
    user_id = message.from_user.id

    bot.send_message(ADMIN_ID,
                     f"📩 Yangi xabar!\n\n👤 ID: {user_id}\n💬 {message.text}")

    bot.send_message(message.chat.id, "✅ Xabaringiz yuborildi!")
# ================== ADMIN PANEL ==================
@bot.message_handler(func=lambda m: m.text == "⚙️ Admin panel")
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👥 Userlar", "📨 Xabar yuborish")
    markup.row("💬 Javob berish", "💰 Balans qo‘shish")
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, "⚙️ Admin panel", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == "📨 Xabar yuborish")
def broadcast_start(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(message.chat.id, "Xabarni yozing:")
    bot.register_next_step_handler(msg, send_broadcast)
def send_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return

    global users

    count = 0

    for user in users:
        try:
            bot.send_message(user["id"], message.text)
            count += 1
        except Exception as e:
            print("Xato:", e)

    bot.send_message(message.chat.id, f"✅ {count} ta userga yuborildi")
@bot.message_handler(func=lambda m: m.text == "👥 Userlar")
def show_users(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    text = "👥 Userlar ro‘yxati:\n\n"

    for i, user in enumerate(users, start=1):
        text += f"{i}. {user.get('name')} | ID: {user.get('id')}\n"

    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda m: m.text == "💰 Balans qo‘shish")
def add_balance_start(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(message.chat.id, "👤 User ID ni yubor:")
    bot.register_next_step_handler(msg, get_user_id)


def get_user_id(message):
    try:
        user_id = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID")
        return

    msg = bot.send_message(message.chat.id, "💰 Summani kiriting:")
    bot.register_next_step_handler(msg, process_balance, user_id)


def process_balance(message, user_id):
    try:
        amount = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri summa")
        return

    global users

    found = False

    for user in users:
        if user.get("id") == user_id:
            user["balance"] = user.get("balance", 0) + amount
            found = True
            break

    if not found:
        bot.send_message(message.chat.id, "❌ User topilmadi")
        return

    with open("users.json", "w") as f:
        json.dump(users, f)

    bot.send_message(user_id, f"💰 Balansingizga {amount} so‘m qo‘shildi!")
    bot.send_message(message.chat.id, "✅ Balans qo‘shildi")


# ================== ADMIN JAVOB ==================
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.reply_to_message)
def admin_reply(message):
    try:
        user_id = int(message.reply_to_message.text.split("ID: ")[1].split("\n")[0])

        bot.send_message(user_id, f"📩 Admin javobi:\n\n{message.text}")

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Xatolik!")

import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# ⭐ Pre-checkout
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_q):
    bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# ⭐ To‘lov muvaffaqiyatli bo‘lsa
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    user_id = message.from_user.id
    stars = message.successful_payment.total_amount

    for user in users:
        if user.get("id") == user_id:
            user["stars"] = user.get("stars", 0) + stars
            break

    with open("users.json", "w") as f:
        json.dump(users, f)

    bot.send_message(
        message.chat.id,
        f"✅ To‘lov qabul qilindi!\n⭐ {stars} Stars qo‘shildi"
    )

bot.infinity_polling()
