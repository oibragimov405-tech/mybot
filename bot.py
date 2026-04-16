import telebot
from telebot import types
from datetime import datetime

CHANNEL = -1003705539547

TOKEN = "8301712601:AAEZ34ynaBuozjubA7N5PF6mW3WIK4iaDRM"
ADMIN_ID = 8360625353

import json
try:
   with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = []
try:
    with open("promocodes.json", "r") as f:
        promocodes = json.load(f)
except:
    promocodes = []

users = [u for u in users if isinstance(u, dict)]
for u in users:
    u.setdefault("used_promos", [])

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
@bot.callback_query_handler(func=lambda call: call.data in ["tg", "insta", "back"])
def callback_main(call):

    if call.data == "tg":
        bot.send_message(call.message.chat.id, "📱 Telegram xizmatlari")

    elif call.data == "insta":
        bot.send_message(call.message.chat.id, "📸 Instagram xizmatlari")

    elif call.data == "back":
        bot.send_message(call.message.chat.id, "🏠 Menu")
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    user_id = call.from_user.id

    if check_subscribe(user_id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi!")

        # ❗ Eski xabarni o‘chiramiz (inline tugmalar ham ketadi)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        # 👇 START funksiyani avtomatik chaqiramiz
        fake_message = call.message
        start(fake_message)

    else:
        bot.answer_callback_query(
            call.id,
            "❌ Hali obuna bo‘lmagansiz!",
            show_alert=True
        )    
@bot.callback_query_handler(func=lambda call: call.data == "stars")
def stars_callback(call):

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⭐ Stars", callback_data="stars_buy"),
        types.InlineKeyboardButton("🎁 Gift", callback_data="gift"),
        types.InlineKeyboardButton("💎 Premium", callback_data="premium")
    )

    bot.edit_message_text(
        "📦 Tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )     
@bot.callback_query_handler(func=lambda call: call.data == "stars_buy")
def stars_buy(call):
    bot.edit_message_text(
        "⭐ Stars bo‘limi",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
@bot.callback_query_handler(func=lambda call: call.data == "gift")
def gift(call):
    bot.edit_message_text(
        "🎁 Username yuboring:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
@bot.callback_query_handler(func=lambda call: call.data == "premium")
def premium(call):

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("1 oy", callback_data="p1"),
        types.InlineKeyboardButton("3 oy", callback_data="p3"),
        types.InlineKeyboardButton("6 oy", callback_data="p6"),
        types.InlineKeyboardButton("12 oy", callback_data="p12"),
    )

    bot.edit_message_text(
        "💎 Tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )                                   

# ================== START ==================
@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscribe(message.from_user.id):
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "📢 Obuna bo‘lish",
                url="https://t.me/nexoweivnews"
            )
        )
        markup.add(
            types.InlineKeyboardButton(
                "✅ Tekshirish",
                callback_data="check_sub"
            )
        )

        bot.send_message(
            message.chat.id,
            "❗ Avval kanalga obuna bo‘ling:",
            reply_markup=markup
        )
        return

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
    "stars": 0,
    "user_today_orders": 0,
    "user_today_spent": 0,
    "user_today_numbers": 0,
    "user_today_stars": 0,
    "used_promos": []
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

    # ✅ MUHIM: ichida bo‘lishi kerak
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("💳 Karta (Avtomatik)", callback_data="card")
    )
    markup.add(
        types.InlineKeyboardButton("⭐ Stars (Avtomatik)", callback_data="stars_pay")
    )
    markup.add(
        types.InlineKeyboardButton("🧑‍💻 Admin orqali", callback_data="admin_pay")
    )
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="back_menu")
    )

    # ✅ TO‘G‘RI INDENT
    bot.send_message(message.chat.id, text, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == "promo_accept")
def promo_input(call):
    msg = bot.send_message(call.message.chat.id, "🎟 Promokodni kiriting:")
    bot.register_next_step_handler(msg, use_promo)    
@bot.callback_query_handler(func=lambda call: call.data in ["card", "stars_pay", "admin_pay", "back_menu"])
def deposit_buttons(call):

    if call.data == "card":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💳 Karta orqali to‘lov tez orada...")

    elif call.data == "stars_pay":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(
            call.message.chat.id,
             "🌟 Nechta Stars kiritasiz?\n\nMinimal miqdor 1🌟"
        )
        bot.register_next_step_handler(msg, process_stars)

    elif call.data == "admin_pay":
        bot.answer_callback_query(call.id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "✍️ Adminga yozish",
            url="https://t.me/smmgarand"
        ))

        bot.send_message(
            call.message.chat.id,
            "👨‍💻 Admin orqali to‘lov:",
            reply_markup=markup
        )

    elif call.data == "back_menu":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🏠 Menu")
# ⭐ Stars tugma bosilganda
@bot.message_handler(func=lambda m: m.text == "⭐ Stars (Avtomatik)")
def stars_input(message):
    msg = bot.send_message(
        message.chat.id,
        "🌟 Nechta Stars to‘lamoqchisiz?\n\nMinimal miqdor: 1 ⭐"
    )
    bot.register_next_step_handler(msg, process_stars)
def process_stars(message):
    try:
        amount = int(message.text)

        if amount < 1:
            bot.send_message(message.chat.id, "❌ Minimal 1 ⭐")
            return

        som = amount * 120  # 💰 hisoblash

        bot.send_invoice(
            message.chat.id,
            "⭐ Stars sotib olish",
            f"{amount} ⭐ = {som} so‘m qo‘shiladi",  # 👈 ENG MUHIM QATOR
            f"stars_{amount}",
            "",
            "XTR",
            [types.LabeledPrice(f"{amount} Stars", amount)]
        )

    except:
        bot.send_message(message.chat.id, "❌ Raqam kiriting!")    
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
@bot.message_handler(func=lambda m: m.text == "⭐ Stars / Gift")
def stars_gift_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("⭐ Stars", "🎁 Premium Gift")
    markup.row("🔙 Orqaga")

    bot.send_message(
        message.chat.id,
        "🎁 Gift bo‘limi:\nTanlang 👇",
        reply_markup=markup
    )
@bot.message_handler(func=lambda m: m.text == "🎁 Premium Gift")
def premium_start(message):
    msg = bot.send_message(message.chat.id, "Necha oy? (1/3/6/12)")
    bot.register_next_step_handler(msg, premium_time)

def premium_time(message):
    prices = {"1":50000,"3":140000,"6":260000,"12":480000}

    if message.text not in prices:
        bot.send_message(message.chat.id, "❌ Xato")
        return

    price = prices[message.text]

    msg = bot.send_message(message.chat.id, "Username yubor:")
    bot.register_next_step_handler(msg, premium_confirm, message.text, price)

def premium_confirm(message, months, price):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "✅ Tasdiqlash",
        callback_data=f"premium_{months}_{price}_{message.text}"
    ))

    bot.send_message(message.chat.id, "Tasdiqlash👇", reply_markup=markup)    

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

    markup = types.InlineKeyboardMarkup()

    markup.add(
    types.InlineKeyboardButton("🎟 Promokod", callback_data="promo")
)
    markup.add(
    types.InlineKeyboardButton("💸 Pul ishlash", callback_data="earn")
)
    markup.add(
    types.InlineKeyboardButton("➡️ Pul o‘tkazish", callback_data="transfer")
)
    markup.add(
    types.InlineKeyboardButton("🔙 Orqaga", callback_data="back_menu")
)

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

    markup.row("📊 Statistika", "🏆 Top userlar")
    markup.row("👥 Userlar", "🔍 User qidirish")
    markup.row("📨 Xabar yuborish", "📢 Aktivlarga xabar")
    markup.row("💰 Balans boshqaruvi", "🚫 Ban boshqaruvi")
    markup.row("🔄 Reset statistika")
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, "⚙️ PRO Admin panel", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == "🚫 Ban boshqaruvi")
def ban_menu(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🚫 Ban qilish", "✅ Unban qilish")
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, "🚫 Ban sozlamalari:", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == "💰 Balans boshqaruvi")
def balance_menu(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("➕ Balans qo‘shish", "➖ Balans ayirish")
    markup.row("🎟 Promokod")
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, "💰 Balans sozlamalari:", reply_markup=markup)   
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


@bot.message_handler(func=lambda m: m.text == "➕ Balans qo‘shish")
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

@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def statistics(message):
    if message.from_user.id != ADMIN_ID:
        return

    from datetime import date
    today = date.today().isoformat()

    total_users = len(users)

    # 🔥 BUGUNGI HISOB
    today_numbers = sum(u.get("user_today_numbers", 0) for u in users)
    today_orders = sum(u.get("user_today_orders", 0) for u in users)
    today_stars = sum(u.get("user_today_stars", 0) for u in users)
    today_income = sum(
        u.get("last_deposit_amount", 0)
        for u in users
        if u.get("last_deposit_date") == today
    )

    text = f"""📊 Bugungi statistika

📅 Sana: {today}

📞 Virtual raqamlar:
📦 Sotildi: {today_numbers} ta
💰 Qiymati: 0 so‘m

🚀 SMM Nakrutka:
📦 Buyurtmalar: {today_orders} ta
💰 Qiymati: 0 so‘m

⭐ Stars & Premium:
📦 Xaridlar: {today_stars} ta
💰 Qiymati: {today_income} so‘m

🔥 Jami bugungi savdo: {today_income} so‘m
"""

    bot.send_message(message.chat.id, text)
@bot.message_handler(func=lambda m: m.text == "🏆 Top userlar")
def top_users(message):
    if message.from_user.id != ADMIN_ID:
        return

    sorted_users = sorted(users, key=lambda x: x.get("deposited", 0), reverse=True)

    text = "🏆 TOP 10 USER:\n\n"

    for i, u in enumerate(sorted_users[:10], 1):
        text += f"{i}. {u.get('name')} — {u.get('deposited',0)} so‘m\n"

    bot.send_message(message.chat.id, text) 
@bot.message_handler(func=lambda m: m.text == "🔍 User qidirish")
def find_user_start(message):
    msg = bot.send_message(message.chat.id, "🔍 User ID yubor:")
    bot.register_next_step_handler(msg, find_user)

def find_user(message):
    try:
        user_id = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID")
        return

    user = next((u for u in users if u.get("id") == user_id), None)

    if not user:
        bot.send_message(message.chat.id, "❌ User topilmadi")
        return

    text = f"""👤 User:

ID: {user_id}
Ism: {user.get("name")}
Username: @{user.get("username")}

💰 Balans: {user.get("balance")} so‘m
📥 Kiritgan: {user.get("deposited")} so‘m
⭐ Stars: {user.get("stars")}
"""

    bot.send_message(message.chat.id, text)
@bot.message_handler(func=lambda m: m.text == "➖ Balans ayirish")
def remove_balance_start(message):
    msg = bot.send_message(message.chat.id, "👤 User ID:")
    bot.register_next_step_handler(msg, remove_balance_user)

def remove_balance_user(message):
    try:
        user_id = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ ID xato")
        return

    msg = bot.send_message(message.chat.id, "💰 Summani kiriting:")
    bot.register_next_step_handler(msg, remove_balance_amount, user_id)

def remove_balance_amount(message, user_id):
    try:
        amount = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri summa")
        return

    for user in users:
        if user.get("id") == user_id:
            user["balance"] = max(0, user.get("balance", 0) - amount)
            break

    with open("users.json", "w") as f:
        json.dump(users, f)

    bot.send_message(message.chat.id, "✅ Balans ayirildi")
@bot.message_handler(func=lambda m: m.text == "🎟 Promokod")
def promo_menu(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("➕ Yaratish", "📜 Tarix")
    markup.row("❌ Bekor qilish", "🔐 Ruxsat boshqaruvi")  # 👈 YANGI
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, "🎟 Promokod boshqaruvi:", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == "🔐 Ruxsat boshqaruvi")
def promo_access_menu(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("✅ Ruxsat berish", "❌ Ruxsatni olish")
    markup.row("📋 Ruxsatli userlar")
    markup.row("🔙 Orqaga")

    bot.send_message(message.chat.id, "🔐 Promokod ruxsat boshqaruvi:", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == "📜 Tarix")
def promo_history(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not promocodes:
        bot.send_message(message.chat.id, "❌ Promokodlar yo‘q")
        return

    text = "📜 Promokodlar tarixi:\n\n"

    for i, p in enumerate(promocodes, 1):
        used = len(p.get("used_by", []))
        limit = p.get("limit", 0)

        text += f"""{i}. 🎟 {p.get("name")}
💰 Bonus: {p.get("amount")} so‘m
👥 Limit: {limit}
📊 Ishlatilgan: {used}/{limit}
🕒 Sana: {p.get("created_at")}

"""
    users_list = p.get("used_by", [])

    if users_list:
        text += "👤 Ishlatganlar:\n"
        for u in users_list[:5]:  # faqat 5 ta ko‘rsatadi
              text += f" - {u}\n"

    # 🔥 agar juda uzun bo‘lsa bo‘lib yuboradi
    if len(text) > 4000:
        for x in range(0, len(text), 4000):
            bot.send_message(message.chat.id, text[x:x+4000])
    else:
        bot.send_message(message.chat.id, text)
@bot.message_handler(func=lambda m: m.text == "✅ Ruxsat berish")
def give_access_start(message):
    msg = bot.send_message(message.chat.id, "👤 User ID yuboring:")
    bot.register_next_step_handler(msg, give_access)


def give_access(message):
    try:
        user_id = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID")
        return

    for user in users:
        if user.get("id") == user_id:
            user["promo_access"] = True

            with open("users.json", "w") as f:
                json.dump(users, f)

            bot.send_message(message.chat.id, "✅ Ruxsat berildi")
            return

    bot.send_message(message.chat.id, "❌ User topilmadi")
@bot.message_handler(func=lambda m: m.text == "❌ Ruxsatni olish")
def remove_access_start(message):
    msg = bot.send_message(message.chat.id, "👤 User ID yuboring:")
    bot.register_next_step_handler(msg, remove_access)


def remove_access(message):
    try:
        user_id = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID")
        return

    for user in users:
        if user.get("id") == user_id:
            user["promo_access"] = False

            with open("users.json", "w") as f:
                json.dump(users, f)

            bot.send_message(message.chat.id, "❌ Ruxsat olib tashlandi")
            return

    bot.send_message(message.chat.id, "❌ User topilmadi")
@bot.message_handler(func=lambda m: m.text == "📋 Ruxsatli userlar")
def show_access_users(message):
    if message.from_user.id != ADMIN_ID:
        return

    text = "🔐 Ruxsatli userlar:\n\n"

    count = 0
    for user in users:
        if user.get("promo_access", False):
            count += 1
            text += f"{count}. {user.get('name')} | ID: {user.get('id')}\n"

    if count == 0:
        text += "❌ Hech kim yo‘q"

    bot.send_message(message.chat.id, text)                
@bot.message_handler(func=lambda m: m.text == "❌ Bekor qilish")
def delete_promo_start(message):
    msg = bot.send_message(message.chat.id, "❌ Qaysi promokodni o‘chirmoqchisiz?\n\nKod nomini kiriting:")
    bot.register_next_step_handler(msg, delete_promo)


def delete_promo(message):
    code = message.text.upper()

    global promocodes

    new_list = [p for p in promocodes if p["name"] != code]

    if len(new_list) == len(promocodes):
        bot.send_message(message.chat.id, "❌ Promokod topilmadi")
        return

    promocodes = new_list

    with open("promocodes.json", "w") as f:
        json.dump(promocodes, f)

    bot.send_message(message.chat.id, "✅ Promokod o‘chirildi")    
@bot.message_handler(func=lambda m: m.text == "➕ Yaratish")
def promo_create_start(message):
    if message.from_user.id != ADMIN_ID:
        return

    msg = bot.send_message(message.chat.id, "🎟 Promokod nomini kiriting:")
    bot.register_next_step_handler(msg, promo_name)    
@bot.message_handler(func=lambda m: m.text == "🚫 Ban qilish")
def ban_user_start(message):
    msg = bot.send_message(message.chat.id, "👤 User ID:")
    bot.register_next_step_handler(msg, ban_user)

def ban_user(message):
    user_id = int(message.text)

    for user in users:
        if user.get("id") == user_id:
            user["banned"] = True
            break

    with open("users.json", "w") as f:
        json.dump(users, f)

    bot.send_message(message.chat.id, "🚫 User ban qilindi")
@bot.message_handler(func=lambda m: m.text == "✅ Unban qilish")
def unban_user_start(message):
    msg = bot.send_message(message.chat.id, "👤 User ID:")
    bot.register_next_step_handler(msg, unban_user)

def unban_user(message):
    user_id = int(message.text)

    for user in users:
        if user.get("id") == user_id:
            user["banned"] = False
            break

    with open("users.json", "w") as f:
        json.dump(users, f)

    bot.send_message(message.chat.id, "✅ User unban qilindi")
@bot.message_handler(func=lambda m: m.text == "📢 Aktivlarga xabar")
def active_broadcast_start(message):
    msg = bot.send_message(message.chat.id, "Xabarni yozing:")
    bot.register_next_step_handler(msg, active_broadcast)

def active_broadcast(message):
    count = 0

    for user in users:
        if user.get("user_today_spent", 0) > 0:
            try:
                bot.send_message(user["id"], message.text)
                count += 1
            except:
                pass

    bot.send_message(message.chat.id, f"✅ {count} ta aktiv userga yuborildi")                       

def promo_name(message):
    name = message.text.upper()
    msg = bot.send_message(message.chat.id, "💰 Summasi:")
    bot.register_next_step_handler(msg, promo_amount, name)


def promo_amount(message, name):
    try:
        amount = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Raqam kiriting")
        return

    msg = bot.send_message(message.chat.id, "👥 Limit:")
    bot.register_next_step_handler(msg, promo_limit, name, amount)


def promo_limit(message, name, amount):
    try:
        limit = int(message.text)
    except:
        bot.send_message(message.chat.id, "❌ Raqam kiriting")
        return

    from datetime import datetime

    promo = {
        "name": name,
        "amount": amount,
        "limit": limit,
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "used_by": []
    }

    promocodes.append(promo)

    with open("promocodes.json", "w") as f:
        json.dump(promocodes, f)

    text = f"""🎁 YANGI PROMOKOD!

🎟 Kod: {name}
💰 Bonus: {amount} so‘m
👥 Limit: {limit} ta
📊 Ishlatildi: 0/{limit}

⚡ Shoshiling!"""

    bot.send_message(message.chat.id, text)    

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
    som = stars * 120

    from datetime import date
    today = date.today().isoformat()

    for user in users:
        if user.get("id") == user_id:
            user["stars"] = user.get("stars", 0) + stars
            user["balance"] = user.get("balance", 0) + som
            
            user["deposited"] = user.get("deposited", 0) + som

            # 🔥 BUGUNGI STATISTIKA
            user["user_today_stars"] = user.get("user_today_stars", 0) + stars
            user["user_today_spent"] = user.get("user_today_spent", 0) + som

            # 🔥 BUGUNGI TUSHUM
            user["last_deposit_date"] = today
            user["last_deposit_amount"] = som
            break

    with open("users.json", "w") as f:
        json.dump(users, f)

    bot.send_message(
        message.chat.id,
        f"✅ To‘lov qabul qilindi!\n\n⭐ {stars} Stars\n💰 {som} so‘m balansga qo‘shildi"
    )
def use_promo(message):
    code = message.text.upper()
    user_id = message.from_user.id

    promo = next((p for p in promocodes if p["name"] == code), None)

    if not promo:
        bot.send_message(message.chat.id, "❌ Promokod topilmadi")
        return

    user = next((u for u in users if u.get("id") == user_id), None)

    if not user:
        bot.send_message(message.chat.id, "❌ User topilmadi")
        return

    # 🔒 AGAR OCHILMAGAN BO‘LSA → SHART TEKSHIR
    if not user.get("promo_access", False):
        referrals = user.get("referrals", 0)
        deposited = user.get("deposited", 0)

        if referrals < 5 or deposited < 3000:
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(
                "📖 Qo‘llanma",
                url="https://t.me/nexoweivnews/5"
            ))
            markup.add(types.InlineKeyboardButton(
                "✅ Roziman",
                callback_data="promo_accept"
            ))

            bot.send_message(
                message.chat.id,
                "🚫 Promokod ishlatish uchun shart bajarilmagan!\n\n"
                "👇 Batafsil qo‘llanma:",
                reply_markup=markup
            )
            return

        # ✅ SHART BAJARILDI → DOIM OCHIQ
        user["promo_access"] = True

    # ❌ Oldin ishlatganmi
    if code in user.get("used_promos", []):
        bot.send_message(message.chat.id, "❌ Siz bu promokodni ishlatgansiz")
        return

    # ❌ Limit tugaganmi
    if len(promo["used_by"]) >= promo["limit"]:
        bot.send_message(message.chat.id, "❌ Promokod tugagan")
        return

    # ✅ ISHLATISH
    user["balance"] += promo["amount"]
    user["used_promos"].append(code)
    promo["used_by"].append(user_id)

    # 💾 SAQLASH
    with open("users.json", "w") as f:
        json.dump(users, f)

    with open("promocodes.json", "w") as f:
        json.dump(promocodes, f)

    used = len(promo["used_by"])
    limit = promo["limit"]

    bot.send_message(
        message.chat.id,
        f"""✅ {promo['amount']} so‘m qo‘shildi!

📊 Holat: {used}/{limit} ishlatildi"""
    )
@bot.callback_query_handler(func=lambda call: call.data == "promo_agree")
def promo_agree(call):
    msg = bot.send_message(call.message.chat.id, "🎟 Promokodni kiriting:")
    bot.register_next_step_handler(msg, use_promo)    

bot.infinity_polling()
