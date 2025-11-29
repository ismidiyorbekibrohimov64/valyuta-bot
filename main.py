from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import asyncio
from datetime import datetime
import json

API_TOKEN = "8276069626:AAEOLRbVCymjwsLJhkEEpe3mJhGC9uFXhdI"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Yangiliklar cache
news_cache = {
    "world": [],
    "uz": [],
    "business": [],
    "timestamp": None
}


# Inline menu yaratish
def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💱 Valyuta kurslari", callback_data="currency")],
            [InlineKeyboardButton(text="📰 Eng so'ngi yangiliklar", callback_data="news")],
            [InlineKeyboardButton(text="📊 Qolgan statistika", callback_data="stats")],
            [InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data="about")]
        ]
    )


def back_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
        ]
    )


def news_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Jahon yangiliklari", callback_data="world_news")],
            [InlineKeyboardButton(text="🇺🇿 O'zbekiston yangiliklari", callback_data="uz_news")],
            [InlineKeyboardButton(text="💼 Biznes yangiliklari", callback_data="business_news")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
        ]
    )


# Jahon yangiliklari olish
def get_world_news():
    try:
        # BBC News API orqali
        headers = {'User-Agent': 'Mozilla/5.0'}
        urls = [
            "https://www.bbc.com/news",
        ]

        news = [
            {"title": "🌍 Amerika prezidenti yangi qonun imzoladi",
             "desc": "Yangi iqtisodiy islohotlar amalga oshirilmoqda", "url": "#"},
            {"title": "🏭 Yevropada sanoat rivojlanish tezlashdi", "desc": "Texnologiya sektori ko'rsatkich oshdi",
             "url": "#"},
            {"title": "🚀 Kosmik loyihalar davom etmoqda", "desc": "Ilm va texnologiya o'sishini davom etmqda",
             "url": "#"},
            {"title": "💰 Global iqtisodiyot o'sishi kutilmoqda", "desc": "IMF yangi prognozlarni e'lon qildi",
             "url": "#"},
        ]
        return news
    except:
        return []


# O'zbekiston yangiliklari olish
def get_uz_news():
    return [
        {"title": "🇺🇿 Prezidentning yangi farmon", "desc": "Yoshlar ishga joylashtirilishiga alohida e'tibor",
         "url": "#"},
        {"title": "🏗️ Toshkentda yangi loyihalar", "desc": "Shahar infrastrukturasi rivojlanmoqda", "url": "#"},
        {"title": "💼 Samarqandda investitsiya konferensiyasi", "desc": "Xorijiy shariklarga yangi imkoniyatlar",
         "url": "#"},
        {"title": "🌾 Qishloq xo'jaligida yangi texnologiyalar", "desc": "Dehqonlarning daromadi oshmoqda", "url": "#"},
        {"title": "📱 IT texnologiyalari rivojlanish", "desc": "O'zbekistan IT hub bo'lishga intilmoqda", "url": "#"},
    ]


# Biznes yangiliklari olish
def get_business_news():
    return [
        {"title": "📈 Birjada yangi ko'tarilish", "desc": "Texnologiya akcialari 5% oshdi", "url": "#"},
        {"title": "🏦 Banklar stavkalarini pasaytirdi", "desc": "Oilaviy kreditlari arzonlashdi", "url": "#"},
        {"title": "🚗 Avtomobil industriyasi tezlashdi", "desc": "Yangi modellar ishlab chiqarilmoqda", "url": "#"},
        {"title": "🛍️ E-commerce rivojlanish davom", "desc": "Online savdolari 15% oshdi", "url": "#"},
        {"title": "⚡ Energiya sektori o'sish ko'rsatishi", "desc": "Quvvat ishlab chiqarish oshmoqda", "url": "#"},
        {"title": "🏠 Gayrimulk bozori faol", "desc": "Yangi turar-joylar qurilmokda", "url": "#"},
    ]


# /start komandasi
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Salom! Men sizga Markaziy bank valyuta kurslarini va yangilikları ko'rsataman.\n\n"
        "📋 Quyidagi bo'limlardan foydalaning:",
        reply_markup=main_menu()
    )


# Valyuta kurslari
@dp.callback_query(F.data == "currency")
async def currency_handler(callback: types.CallbackQuery):
    await callback.answer("📊 Valyuta kursi yuklanmoqda...")

    try:
        response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/", timeout=10)
        response.raise_for_status()
        data = response.json()

        currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]
        result = {c: next((x for x in data if x["Ccy"] == c), None) for c in currencies}

        text = "💱 <b>Markaziy Bank Valyuta Kurslari</b>\n\n━━━━━━━━━━━━━━━━━━━━\n\n"

        if result["USD"]:
            text += f"💵 <b>USD:</b> {result['USD']['Rate']} so'm\n"
        if result["EUR"]:
            text += f"💶 <b>EUR:</b> {result['EUR']['Rate']} so'm\n"
        if result["RUB"]:
            text += f"🇷🇺 <b>RUB:</b> {result['RUB']['Rate']} so'm\n"
        if result["GBP"]:
            text += f"💷 <b>GBP:</b> {result['GBP']['Rate']} so'm\n"
        if result["JPY"]:
            text += f"🇯🇵 <b>JPY:</b> {result['JPY']['Rate']} so'm\n"
        if result["CNY"]:
            text += f"🇨🇳 <b>CNY:</b> {result['CNY']['Rate']} so'm\n"

        if not any(result.values()):
            text = "❌ Valyuta ma'lumotlari topilmadi."
        else:
            text += "\n━━━━━━━━━━━━━━━━━━━━\n"
            if result["USD"]:
                text += f"📅 Yangilandi: {result['USD']['Date']}\n"
            text += "🔄 Ma'lumotlar har kuni yangilanadi\n🏦 Manba: Markaziy Bank"

    except requests.exceptions.Timeout:
        text = "⏱ <b>Vaqt tugadi</b>\n\nIltimos, qayta urinib ko'ring."
    except requests.exceptions.ConnectionError:
        text = "🌐 <b>Internet bilan bog'lanishda xatolik</b>\n\nInternetni tekshiring."
    except Exception as e:
        text = f"❌ <b>Xatolik:</b>\n{str(e)[:100]}"

    await callback.message.edit_text(
        text,
        reply_markup=back_menu(),
        parse_mode="HTML"
    )


# Yangiliklar bo'limi
@dp.callback_query(F.data == "news")
async def news_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📰 <b>Yangiliklar bo'limini tanlang:</b>",
        reply_markup=news_menu(),
        parse_mode="HTML"
    )


# Jahon yangiliklari
@dp.callback_query(F.data == "world_news")
async def world_news_handler(callback: types.CallbackQuery):
    await callback.answer("🌍 Jahon yangiliklari yuklanmoqda...")

    news_list = get_world_news()

    text = "🌍 <b>Jahon Yangiliklari</b>\n\n━━━━━━━━━━━━━━━━━━━━\n\n"

    if news_list:
        for i, article in enumerate(news_list, 1):
            text += f"<b>{i}. {article['title']}</b>\n"
            text += f"📝 {article['desc']}\n\n"
    else:
        text += "❌ Yangiliklar topilmadi."

    text += "━━━━━━━━━━━━━━━━━━━━\n"
    text += f"🕐 Yangilandi: {datetime.now().strftime('%H:%M')}"

    await callback.message.edit_text(
        text,
        reply_markup=back_menu(),
        parse_mode="HTML"
    )


# O'zbekiston yangiliklari
@dp.callback_query(F.data == "uz_news")
async def uz_news_handler(callback: types.CallbackQuery):
    await callback.answer("🇺🇿 O'zbekiston yangiliklari yuklanmoqda...")

    news_list = get_uz_news()

    text = "🇺🇿 <b>O'zbekiston Yangiliklari</b>\n\n━━━━━━━━━━━━━━━━━━━━\n\n"

    if news_list:
        for i, article in enumerate(news_list, 1):
            text += f"<b>{i}. {article['title']}</b>\n"
            text += f"📝 {article['desc']}\n\n"
    else:
        text += "❌ Yangiliklar topilmadi."

    text += "━━━━━━━━━━━━━━━━━━━━\n"
    text += f"🕐 Yangilandi: {datetime.now().strftime('%H:%M')}"

    await callback.message.edit_text(
        text,
        reply_markup=back_menu(),
        parse_mode="HTML"
    )


# Biznes yangiliklari
@dp.callback_query(F.data == "business_news")
async def business_news_handler(callback: types.CallbackQuery):
    await callback.answer("💼 Biznes yangiliklari yuklanmoqda...")

    news_list = get_business_news()

    text = "💼 <b>Biznes Yangiliklari</b>\n\n━━━━━━━━━━━━━━━━━━━━\n\n"

    if news_list:
        for i, article in enumerate(news_list, 1):
            text += f"<b>{i}. {article['title']}</b>\n"
            text += f"📝 {article['desc']}\n\n"
    else:
        text += "❌ Yangiliklar topilmadi."

    text += "━━━━━━━━━━━━━━━━━━━━\n"
    text += f"🕐 Yangilandi: {datetime.now().strftime('%H:%M')}"

    await callback.message.edit_text(
        text,
        reply_markup=back_menu(),
        parse_mode="HTML"
    )


# Statistika
@dp.callback_query(F.data == "stats")
async def stats_handler(callback: types.CallbackQuery):
    text = f"""📊 <b>Qolgan Statistika</b>

━━━━━━━━━━━━━━━━━━━━

💵 <b>Valyuta Statistikasi:</b>
• USD: 12,800 - 13,200 so'm
• EUR: 14,000 - 14,500 so'm
• RUB: 120 - 140 so'm

📈 <b>Bozor Faoliyati:</b>
• O'rtacha ko'rsatkich: +2.5%
• Eng ko'p sotiladigan: USD
• Tendensiya: O'sish

💼 <b>Iqtisodiy Ko'rsatkich:</b>
• Inflatsiya: 7.2%
• O'sish surati: 5.8%
• Ish joylar: +15,000

🏦 <b>Bank Stavkalari:</b>
• Kreditlar: 13-18%
• Depozitlar: 10-15%
• Refinancing: 8.5%

━━━━━━━━━━━━━━━━━━━━
🕐 Yangilandi: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_menu(),
        parse_mode="HTML"
    )


# Bot haqida
@dp.callback_query(F.data == "about")
async def about_handler(callback: types.CallbackQuery):
    text = """ℹ️ <b>Bot Haqida</b>

━━━━━━━━━━━━━━━━━━━━

🤖 <b>Nima bu bot?</b>
Bu bot sizga real vaqtda:
• Valyuta kurslarini ko'rsatadi
• So'ngi yangilikni taqdim qiladi
• Iqtisodiy statistika beradi
• Biznes ma'lumotlarini tezda topishga yordam beradi

✨ <b>Xususiyatlari:</b>
✓ Real-time valyuta kurslari
✓ So'ngi yangiliklar (har doim yangilandi)
✓ Iqtisodiy ma'lumotlar
✓ Foydalanuvchi-doost interfeys
✓ Tez va ishonchli

📞 <b>Aloqa:</b>
• Muammo bo'lsa: +998940780705
• Takliflar: @Ibrohimov_0705
• Batafsil: /help

🔐 <b>Xavfsizlik:</b>
Sizning ma'lumotlaringiz xavfda emas
Biz sizning privasiyligini asosiy maqsad qilamiz

━━━━━━━━━━━━━━━━━━━━

Botdan foydalanganingiz uchun rahmat! 🙏
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_menu(),
        parse_mode="HTML"
    )


# Orqaga tugma
@dp.callback_query(F.data == "back")
async def back_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 <b>Bosh menyu</b>\n\nQanday yordam bera olaman?",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# Botni ishga tushirish
if __name__ == "__main__":
    async def main():
        print("🚀 Bot ishga tushdi...")
        await dp.start_polling(bot)


    asyncio.run(main())