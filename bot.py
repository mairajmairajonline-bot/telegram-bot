import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_LINK = "https://t.me/Amuzesh_cafetradeTvaf/84"

# -------------------- جلسات و کپشن‌ها --------------------
sessions = {
    "intro": {
        "title": "معرفی دوره",
        "file_id": "VIDEO_FILE_ID_INTRO",
        "caption": """آموزش بازار های مالی صفر تا صد:
📚 معرفی دوره
🔹 در این ویدیو درباره شروع دوره و ساختار کامل کورس توضیح داده شده است.
@cafetradetvaf"""
    },
    # فصل اول: ابتدایی
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی", "file_id": "VIDEO_FILE_ID_1_1_1", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه اول: تعریف ساده بازارهای مالی\n✅ توضیح بازار و انواع آن\n@cafetradetvaf"},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی", "file_id": "VIDEO_FILE_ID_1_1_2", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه دوم: ماهیت بازارهای مالی\n✅ بررسی انواع بازارها و مدیریت سرمایه\n@cafetradetvaf"},
    "beg1_1_3": {"title": "جلسه سوم: تریدر کیست", "file_id": "VIDEO_FILE_ID_1_1_3", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه سوم: تریدر کیست\n✅ تفاوت تریدر و سرمایه گذار و نقش هر کدام\n@cafetradetvaf"},
    "beg1_1_4": {"title": "جلسه چهارم: انواع سبک‌های ترید", "file_id": "VIDEO_FILE_ID_1_1_4", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه چهارم: انواع سبک‌های ترید\n✅ آشنایی با سویینگ، اسکالپینگ و دیتریدینگ\n@cafetradetvaf"},
    "beg1_1_5": {"title": "جلسه پنجم: نکات کلیدی برای شروع ترید", "file_id": "VIDEO_FILE_ID_1_1_5", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه پنجم: نکات کلیدی برای شروع ترید\n✅ شروع ترید و چالش‌ها و حقایق بازار\n@cafetradetvaf"},
    "beg1_1_6": {"title": "جلسه ششم: خلاصه و جمع‌بندی", "file_id": "VIDEO_FILE_ID_1_1_6", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه ششم: خلاصه و جمع‌بندی\n✅ مرور تمام جلسات قبلی\n@cafetradetvaf"},
    "beg1_2_1": {"title": "جلسه اول: آشنایی با تحلیل بازار", "file_id": "VIDEO_FILE_ID_1_2_1", "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه اول: آشنایی با تحلیل بازار\n✅ اهمیت تحلیل بازار و زمان‌بندی خرید و فروش\n@cafetradetvaf"},
    "beg1_2_2": {"title": "جلسه دوم: معرفی سبک‌های تحلیلی", "file_id": "VIDEO_FILE_ID_1_2_2", "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه دوم: معرفی سبک‌های تحلیلی\n✅ تحلیل تکنیکال و Price Action، RTM، ICT و Order Flow\n@cafetradetvaf"},
    "beg1_2_3": {"title": "جلسه سوم: اندیکاتورها و سیگنال‌ها", "file_id": "VIDEO_FILE_ID_1_2_3", "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه سوم: اندیکاتورها و سیگنال‌ها\n✅ آشنایی با اندیکاتورها و سیگنال‌های معاملاتی\n@cafetradetvaf"},
    "beg1_2_4": {"title": "جلسه چهارم: تحلیل فاندامنتال", "file_id": "VIDEO_FILE_ID_1_2_4", "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه چهارم: تحلیل فاندامنتال\n✅ اهمیت اخبار اقتصادی و تأثیر آن بر بازار\n@cafetradetvaf"},
    "beg1_2_5": {"title": "جلسه پنجم: تعریف ساده داده‌ها", "file_id": "VIDEO_FILE_ID_1_2_5", "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه پنجم: تعریف ساده داده‌ها\n✅ مفاهیم اقتصادی مانند نرخ بهره و تورم\n@cafetradetvaf"},
    # فصل دوم: پیشرفته
    "beg2_1_1": {"title": "جلسه اول: تحلیل تکنیکال پیشرفته", "file_id": "VIDEO_FILE_ID_2_1_1", "caption": "📚 فصل دوم: پیشرفته\n📊 بخش اول: تحلیل پیشرفته\n🎓 جلسه اول: تحلیل تکنیکال پیشرفته\n✅ ابزارها و الگوهای پیشرفته تکنیکال\n@cafetradetvaf"},
    "beg2_1_2": {"title": "جلسه دوم: مدیریت سرمایه پیشرفته", "file_id": "VIDEO_FILE_ID_2_1_2", "caption": "📚 فصل دوم: پیشرفته\n📊 بخش اول: تحلیل پیشرفته\n🎓 جلسه دوم: مدیریت سرمایه پیشرفته\n✅ تکنیک‌های مدیریت ریسک و سرمایه\n@cafetradetvaf"},
    "beg2_1_3": {"title": "جلسه سوم: روانشناسی معامله‌گر", "file_id": "VIDEO_FILE_ID_2_1_3", "caption": "📚 فصل دوم: پیشرفته\n📊 بخش اول: تحلیل پیشرفته\n🎓 جلسه سوم: روانشناسی معامله‌گر\n✅ کنترل احساسات و تصمیم‌گیری در بازار\n@cafetradetvaf"},
}

# -------------------- ساختار منو --------------------
menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2","beg1_1_3","beg1_1_4","beg1_1_5","beg1_1_6"],
        "بخش دوم: تحلیل بازار": ["beg1_2_1","beg1_2_2","beg1_2_3","beg1_2_4","beg1_2_5"],
    },
    "فصل دوم: پیشرفته": {
        "بخش اول: تحلیل پیشرفته": ["beg2_1_1","beg2_1_2","beg2_1_3"],
    },
    "فصل سوم: پروژه عملی": {},
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً فصل مورد نظر را انتخاب کنید:"

def main_menu_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("معرفی دوره", callback_data="intro")],
        [InlineKeyboardButton("فصل اول: ابتدایی", callback_data="f1")],
        [InlineKeyboardButton("فصل دوم: پیشرفته", callback_data="f2")],
        [InlineKeyboardButton("فصل سوم: پروژه عملی", callback_data="f3")],
        [InlineKeyboardButton("📋 جزئیات بیشتر", url=CHANNEL_LINK)]
    ])

# -------------------- start handler --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup())

# -------------------- button handler --------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    # ارسال ویدیو با کپشن، پیام منو در پایین
    if data in sessions:
        s = sessions[data]
        try:
            await context.bot.send_video(chat_id=chat_id, video=s["file_id"], caption=s["caption"], parse_mode="HTML")
        except TelegramError as e:
            logger.error(f"Failed to send video for {data}: {e}")
            await context.bot.send_message(chat_id=chat_id, text=f"خطا در ارسال ویدیو:\n{e}")
        return

    # منو اصلی
    if data == "main":
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup())
        return

    # معرفی دوره
    if data == "intro":
        s = sessions["intro"]
        try:
            await context.bot.send_video(chat_id=chat_id, video=s["file_id"], caption=s["caption"], parse_mode="HTML")
        except TelegramError as e:
            logger.error(f"Failed to send intro video: {e}")
        return

    # فصل اول
    if data == "f1":
        buttons = [[InlineKeyboardButton(b, callback_data=f"f1_{i}")] for i, b in enumerate(menu_structure["فصل اول: ابتدایی"].keys())]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="main")])
        await query.message.edit_text("فصل اول: ابتدایی\nبخش مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # فصل دوم
    if data == "f2":
        buttons = [[InlineKeyboardButton(b, callback_data=f"f2_{i}")] for i, b in enumerate(menu_structure["فصل دوم: پیشرفته"].keys())]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="main")])
        await query.message.edit_text("فصل دوم: پیشرفته\nبخش مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # فصل سوم
    if data == "f3":
        await query.message.edit_text("این فصل فعلاً در دسترس نیست.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]]))
        return

    # نمایش جلسات بخش‌ها
    if "_" in data and data[0] == "f":
        f_key, idx = data.split("_", 1)
        idx = int(idx)
        if f_key == "f1":
            section_name = list(menu_structure["فصل اول: ابتدایی"].keys())[idx]
            sessions_list = menu_structure["فصل اول: ابتدایی"][section_name]
            buttons = [[InlineKeyboardButton(sessions[s]["title"], callback_data=s)] for s in sessions_list]
            buttons.append([InlineKeyboardButton("بازگشت", callback_data="f1")])
            await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        elif f_key == "f2":
            section_name = list(menu_structure["فصل دوم: پیشرفته"].keys())[idx]
            sessions_list = menu_structure["فصل دوم: پیشرفته"][section_name]
            buttons = [[InlineKeyboardButton(sessions[s]["title"], callback_data=s)] for s in sessions_list]
            buttons.append([InlineKeyboardButton("بازگشت", callback_data="f2")])
            await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))

# -------------------- main --------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling update:", exc_info=context.error)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    logger.info("Bot is running...")
    print("Bot is running...")
    app.run_polling()