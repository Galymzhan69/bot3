import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ==================== БАПТАУЛАР ====================
BOT_TOKEN = "8761520469:AAHBhQ0YC27HQgHXQALflferH8rJ5D6qqzw"  # BotFather-ден алған токенді қойыңыз
ADMIN_ID = 8129855972  # Өзіңіздің Telegram ID-іңізді жазыңыз (@userinfobot арқылы білуге болады)
MANAGER_USERNAME = "from_aksh"  # Менеджердің юзернеймі

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База деректерін қарапайым жадта сақтау (Статистика үшін)
all_users = set()
today_users = set()
last_reset_date = datetime.now().date()

# ==================== ДЕРЕКТЕР БАЗАСЫ (WAKA) ====================
WAKA_PRODUCTS = {
    "waka_6000": {
        "name": "WAKA Smash 6000",
        "puffs": "6 000 затяжек",
        "price": "8 500 ₸",
        "info": "Закрывает импульсный спрос и покупателей, которым не нужен большой ресурс.",
        "flavors": ["Watermelon Ice", "Strawberry Banana", "Mango Orange", "Melon Ice", "Banana Ice"]
    },
    "waka_9000_boost": {
        "name": "WAKA Novo Boost 9000",
        "puffs": "9 000 затяжек",
        "price": "11 500 ₸",
        "info": "Компактный дизайн, быстрый нагрев и насыщенный вкус.",
        "flavors": ["Blueberry Raspberry", "Peach Ice", "Fresh Mint", "Watermelon", "Strawberry Kiwi"]
    },
    "waka_9000_gala": {
        "name": "WAKA Novo Gala 9000",
        "puffs": "9 000 затяжек",
        "price": "11 500 ₸",
        "info": "Яркий корпус и стабильная передача вкуса.",
        "flavors": ["Grape Ice", "Berry Blast", "Blackberry Lemon", "Double Apple"]
    },
    "waka_8000": {
        "name": "WAKA SLIM 8000",
        "puffs": "8 000 затяжек",
        "price": "10 500 ₸",
        "info": "Дает понятную середину без переплаты за верхний сегмент.",
        "flavors": ["Strawberry Watermelon", "Cherry Lemon", "Tropical Punch", "Mango Ice"]
    },
    "waka_10000": {
        "name": "WAKA soPro PA10000",
        "puffs": "10 000 затяжек",
        "price": "12 500 ₸",
        "info": "Двойной койл (Boost режим) және мықты өнімділік.",
        "flavors": ["Triple Berry", "Fresh Mint", "Dark Grape", "Kiwi Passion Fruit"]
    },
    "waka_15000": {
        "name": "Waka XLand 15000",
        "puffs": "15 000 затяжек",
        "price": "17 500 ₸",
        "info": "Орташа ресурс іздеушілерге арналған сенімді таңдау.",
        "flavors": ["Watermelon Ice", "Strawberry Dragonfruit", "Blackberry Ice", "Cola Lime"]
    },
    "waka_20000": {
        "name": "WAKA soPro 20000",
        "puffs": "20 000 затяжек",
        "price": "22 500 ₸",
        "info": "Удерживает тех, кто уже смотрит на длительное использование.",
        "flavors": ["Dark Blackcurrant Ice", "Grape Burst", "Energy Drink", "Green Apple"]
    },
    "waka_25000": {
        "name": "Waka XLand PA25000",
        "puffs": "25 000 затяжек",
        "price": "27 500 ₸",
        "info": "Үлкен экран және қуатты аккумулятор.",
        "flavors": ["Tropical Blast", "Double Apple", "Strawberry Banana", "Watermelon Chill"]
    },
    "waka_30000": {
        "name": "WAKA Jupiter 30000",
        "puffs": "30 000 затяжек",
        "price": "32 500 ₸",
        "info": "Флагмандық сыйымдылық және реттелетін тартылым.",
        "flavors": ["Peach Mango", "Cherry Cola", "Cool Mint", "Blue Razz"]
    },
    "waka_60000": {
        "name": "WAKA Double 60000",
        "puffs": "60 000 затяжек",
        "price": "62 500 ₸",
        "info": "Максимальный запас. Закрывает запрос на большой ресурс.",
        "flavors": ["Watermelon + Mint", "Blueberry + Mango", "Tropical Duo", "Cherry Lemonade Duo"]
    }
}

# Статистиканы күн сайын жаңарту функциясы
def check_daily_reset():
    global last_reset_date, today_users
    now = datetime.now().date()
    if now > last_reset_date:
        today_users.clear()
        last_reset_date = now

# ==================== ХЭНДЛЕРЛЕР (ӨҢДЕУШІЛЕР) ====================

# 1. /start Командасы - Негізгі меню
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    check_daily_reset()
    user_id = message.from_user.id
    all_users.add(user_id)
    today_users.add(user_id)

    builder = InlineKeyboardBuilder()
    builder.button(text="💨 Заказать Разку", callback_data="catalog")
    builder.button(text="🎮 Игры", callback_data="games")
    
    # Егер қолданушы админ болса, 3-ші батырма қосылады
    if user_id == ADMIN_ID:
        builder.button(text="📊 Админ Статистика", callback_data="admin_stats")
        
    builder.adjust(1)
    
    await message.answer(
        "Саламатсыз ба! Төмендегі батырмалар арқылы қажетті бөлімді таңдаңыз:",
        reply_markup=builder.as_markup()
    )

# 2. "Заказать Разку" - Өнімдер тізімі
@dp.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    
    for key, product in WAKA_PRODUCTS.items():
        builder.button(text=product["name"], callback_data=f"prod_{key}")
        
    builder.button(text="⬅️ Артқа", callback_data="main_menu")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Қажетті WAKA моделін таңдаңыз:",
        reply_markup=builder.as_markup()
    )

# 3. Жеке ВАКА-ны таңдағанда (Ақпарат + Вкустар)
@dp.callback_query(F.data.startswith("prod_"))
async def show_product_details(callback: types.CallbackQuery):
    product_key = callback.data.replace("prod_", "")
    product = WAKA_PRODUCTS.get(product_key)
    
    if not product:
        return

    text = (
        f"📱 **{product['name']}** ({product['puffs']})\n\n"
        f"💰 **Бағасы:** {product['price']}\n"
        f"ℹ️ **Ақпарат:** {product['info']}\n\n"
        f"👇 Қалаған вкусыңызды таңдаңыз:"
    )
    
    builder = InlineKeyboardBuilder()
    
    # Вкустарды батырма ретінде шығару
    for idx, flavor in enumerate(product["flavors"]):
        builder.button(text=f"🍋 {flavor}", callback_data=f"buy_{product_key}_{idx}")
        
    builder.button(text="⬅️ Модельдерге артқа", callback_data="catalog")
    builder.adjust(1)
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")

# 4. Вкус басылғанда - Менеджерге сілтеме жасау (Авто-текстпен)
@dp.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery):
    data_parts = callback.data.split("_")
    product_key = f"{data_parts[1]}_{data_parts[2]}" if len(data_parts) == 4 else f"{data_parts[1]}_{data_parts[2]}_{data_parts[3]}"
    flavor_idx = int(data_parts[-1])
    
    product = WAKA_PRODUCTS.get(product_key)
    flavor_name = product["flavors"][flavor_idx]
    
    # Дайын сәлемдесу мәтіні (URL encode)
    msg_text = f"Сәлеметсіз бе! Мен {product['name']} ({flavor_name}) алғым келеді."
    encoded_text = msg_text.replace(" ", "%20")
    
    # Менеджер личкасына өтетін Telegram link
    link = f"https://t.me/{MANAGER_USERNAME}?text={encoded_text}"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📩 Менеджерге жазу", url=link)
    builder.button(text="⬅️ Артқа", callback_data=f"prod_{product_key}")
    builder.adjust(1)
    
    await callback.message.edit_text(
        f"✅ Тандаған өнім:\n**{product['name']}**\nВкус: **{flavor_name}**\nБағасы: **{product['price']}**\n\n"
        f"Тапсырысты аяқтау үшін төмендегі батырманы басып менеджерге өтіңіз:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

# 5. "Игры" бөлімі
@dp.callback_query(F.data == "games")
async def show_games(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🎲 Сүйек лақтыру (Dice)", callback_data="play_dice")
    builder.button(text="🎰 Ойын автоматы (Slots)", callback_data="play_slots")
    builder.button(text="⬅️ Бас меню", callback_data="main_menu")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Зерікпеу үшін ойын түрін таңдаңыз:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("play_"))
async def play_game(callback: types.CallbackQuery):
    game_type = callback.data.replace("play_", "")
    emoji = "🎲" if game_type == "dice" else "🎰"
    
    await callback.message.delete()
    await callback.message.answer_dice(emoji=emoji)
    
    # Қайта менюді көрсету
    await asyncio.sleep(2)
    builder = InlineKeyboardBuilder()
    builder.button(text="🎮 Тағы ойнау", callback_data="games")
    builder.button(text="🏠 Бас меню", callback_data="main_menu")
    builder.adjust(1)
    await callback.message.answer("Ойын аяқталды!", reply_markup=builder.as_markup())

# 6. Админ статистикасы (Тек Админге)
@dp.callback_query(F.data == "admin_stats")
async def show_stats(callback: types.CallbackQuery):
    check_daily_reset()
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Бұл бөлім тек админге арналған!", show_alert=True)
        return
        
    text = (
        "📊 **Бот Статистикасы:**\n\n"
        f"👤 Жалпы қолданушылар: **{len(all_users)}**\n"
        f"📅 Бүгін кіргендер: **{len(today_users)}**"
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Артқа", callback_data="main_menu")
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")

# 7. Бас менюге қайту
@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="💨 Заказать Разку", callback_data="catalog")
    builder.button(text="🎮 Игры", callback_data="games")
    
    if callback.from_user.id == ADMIN_ID:
        builder.button(text="📊 Админ Статистика", callback_data="admin_stats")
        
    builder.adjust(1)
    await callback.message.edit_text("Бас меню:", reply_markup=builder.as_markup())

# ==================== БОТТЫ ІСКЕ ҚОСУ ====================
async def main():
    print("Бот іске қосылды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())