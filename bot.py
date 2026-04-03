import telebot
from telebot import types
import json

BOT_TOKEN = "8301712601:AAGr5EtrnRA7dAA46y0u5Qw6MqelZnB4s3s"
ADMIN_ID = 123456789

bot = telebot.TeleBot(BOT_TOKEN)

# ===== USERS =====
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

users = load_users()

def get_user_id(tg_id):
    tg_id = str(tg_id)
    if tg_id not in users:
        users[tg_id] = len(users) + 1
        save_users(users)
    return users[tg_id]

# ===== ORDERS =====
def load_orders():
    try:
        with open("orders.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_orders(orders):
    with open("orders.json", "w") as f:
        json.dump(orders, f)

orders = load_orders()

def create_order(uid):
    uid = str(uid)

    if uid not in orders:
        orders[uid] = 0

    orders[uid] += 1
    save_orders(orders)

    return f"{int(uid):02d}{orders[uid]:02d}"

ratings = {}

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    uid = get_user_id(message.from_user.id)

    text = f"""╔═══ 👋 Assalomu Alaykum ═══╗

🤖 @nexoviewbot ga xush kelibsiz!

🌐 Bot orqali siz:

━━━━━━━━━━━━━━━━━━━
📱 Virtual nomerlar  
📈 Nakrutka xizmatlari  
⭐ Telegram Premium  
✨ Telegram Stars  
━━━━━━━━━━━━━━━━━━━

⚡ Tezkor • 🔒 Ishonchli • 💸 Qulay  

📩 Kerakli bo‘limni tanlang 👇

╚═══════════════════╝
"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📱 Nomer olish", "📊 Xizmatlar")
    markup.add("📖 Qo‘llanma", "⭐ Baholash")
    markup.add("📞 Admin")

    bot.send_message(message.chat.id, text, reply_markup=markup)

# ===== NOMER INLINE =====
@bot.message_handler(func=lambda m: m.text == "📱 Nomer olish")
def nomer(message):
    markup = types.InlineKeyboardMarkup()

    countries = [
        ("🇺🇿 O‘zbekiston", "uz"),
        ("🇷🇺 Rossiya", "ru"),
        ("🇺🇸 AQSH", "us"),
        ("🇹🇷 Turkiya", "tr"),
        ("🇮🇳 Hindiston", "in"),
        ("🇩🇪 Germaniya", "de"),
        ("🇫🇷 Fransiya", "fr"),
        ("🇮🇹 Italiya", "it"),
        ("🇪🇸 Ispaniya", "es"),
        ("🇰🇿 Qozog‘iston", "kz"),
        ("🇰🇷 Koreya", "kr"),
        ("🇯🇵 Yaponiya", "jp"),
        ("🇸🇦 Saudiya", "sa"),
        ("🇧🇷 Braziliya", "br"),
        ("🇮🇩 Indoneziya", "id"),
        ("🇵🇰 Pokiston", "pk"),
        ("🇧🇩 Bangladesh", "bd"),
        ("🇪🇬 Misr", "eg"),
    ]

    for name, code in countries:
        markup.add(types.InlineKeyboardButton(name, callback_data=f"country_{code}"))

    bot.send_message(message.chat.id, "🌍 Davlatni tanlang:", reply_markup=markup)

# ===== COUNTRY TANLANGANDA =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
def country_selected(call):
    uid = get_user_id(call.from_user.id)
    order_id = create_order(uid)

    country = call.data.split("_")[1]

    text = f"""📦 Yangi buyurtma!

🆔 User ID: {uid}
📄 Buyurtma ID: {order_id}
🌍 Davlat: {country.upper()}
"""

    bot.send_message(ADMIN_ID, text)
    bot.answer_callback_query(call.id, "✅ Buyurtma yuborildi!")

    bot.send_message(call.message.chat.id, f"""✅ Buyurtma qabul qilindi!

📄 Buyurtma ID: {order_id}
📞 Tez orada admin bog‘lanadi
""")

# ===== XIZMATLAR =====
@bot.message_handler(func=lambda m: m.text == "📊 Xizmatlar")
def xizmatlar(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⭐ Premium", "✨ Stars")
    markup.add("🔙 Orqaga")

    bot.send_message(message.chat.id, "📦 Xizmatlar:", reply_markup=markup)

# ===== QOLLANMA =====
@bot.message_handler(func=lambda m: m.text == "📖 Qo‘llanma")
def qollanma(message):
    bot.send_message(message.chat.id, """📖 QO‘LLANMA

1️⃣ Nomer olish → davlat tanlang  
2️⃣ Xizmatlar → Premium / Stars  
3️⃣ Admin → murojaat  
4️⃣ Baholash → baho bering  

⚡ Oson va tez!
""")

# ===== ADMIN =====
@bot.message_handler(func=lambda m: m.text == "📞 Admin")
def admin(message):
    bot.send_message(message.chat.id, "✍️ Xabaringizni yozing:")

    bot.register_next_step_handler(message, send_to_admin)

def send_to_admin(message):
    uid = get_user_id(message.from_user.id)

    text = f"""📩 Murojaat

🆔 User ID: {uid}
💬 {message.text}
"""

    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ Yuborildi!")

# ===== BAHOLASH =====
@bot.message_handler(func=lambda m: m.text == "⭐ Baholash")
def rate(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1⭐", "2⭐", "3⭐", "4⭐", "5⭐")

    bot.send_message(message.chat.id, "⭐ Baho bering:", reply_markup=markup)

@bot.message_handler(func=lambda m: "⭐" in m.text)
def save_rate(message):
    ratings[message.from_user.id] = message.text
    bot.send_message(message.chat.id, "🙏 Raxmat!")

# ===== ADMIN PANEL =====
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        total_users = len(users)

        bot.send_message(message.chat.id, f"""📊 ADMIN PANEL

👥 Foydalanuvchilar: {total_users}
📦 Buyurtmalar: {sum(orders.values())}
""")

# ===== RUN =====
bot.infinity_polling()
