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

# --- جلسات فصل اول و دوم با کپشن ---
sessions = {
    "intro": {"title": "معرفی دوره", "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA",
              "caption": "📚 معرفی دوره\n🔹 در این ویدیو درباره شروع دوره و ساختار کامل کورس توضیح داده شده است.\n@cafetradetvaf"},
    # فصل اول: ابتدایی - بخش بازارهای مالی
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی", "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA",
                 "caption": "✅ تعریف ساده بازار و انواع بازارها\n@cafetradetvaf"},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی", "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ",
                 "caption": "✅ انواع بازارهای مالی و مدیریت سرمایه\n@cafetradetvaf"},
    "beg1_1_3": {"title": "جلسه سوم: تریدر کیست", "file_id": "BAACAgUAAxkBAAMXacguqjFHva0sNJqMQU823xJWsiAAAlEdAAK-qZhVfgocOT6_1gk6BA",
                 "caption": "✅ ترید چیست، تریدر کیست، تفاوت با سرمایه‌گذار\n@cafetradetvaf"},
    "beg1_1_4": {"title": "جلسه چهارم: انواع سبک‌های ترید", "file_id": "BAACAgUAAxkBAAMYacguqgFRh3FlotgC-HMkPimgGlwAAg8dAAIpZ7BVHnpO0EQ-0Jc6BA",
                 "caption": "✅ انواع سبک‌های ترید: سویینگ، اسکالپینگ، دیتریدینگ\n@cafetradetvaf"},
    "beg1_1_5": {"title": "جلسه پنجم: نکات کلیدی برای شروع ترید", "file_id": "BAACAgUAAxkBAAMZacguqkRSe_qBmbMqVYFmLcwGHZ4AAkAeAAIaGrBVrvNEiiRia-A6BA",
                 "caption": "✅ بررسی واقعیت‌های شروع ترید و نکات مهم\n@cafetradetvaf"},
    "beg1_1_6": {"title": "جلسه ششم: خلاصه و جمع‌بندی", "file_id": "BAACAgUAAxkBAAMaacguqsV443jxKgTT3roWGBBeh8wAAlseAAIaGrBV6SJRv8Q1eDw6BA",
                 "caption": "✅ جمع‌بندی نکات کلیدی جلسات قبل\n@cafetradetvaf"},
    # فصل اول: ابتدایی - بخش تحلیل بازار
    "beg1_2_1": {"title": "جلسه اول: آشنایی با تحلیل بازار", "file_id": "BAACAgUAAxkBAAMbacguqsR5nOj-1SOzWPiKE80uTLYAAjIcAAIRfclVy88EIhjFgDE6BA",
                 "caption": "✅ مفهوم تحلیل بازار و تشخیص زمان خرید و فروش\n@cafetradetvaf"},
    "beg1_2_2": {"title": "جلسه دوم: معرفی سبک‌های تحلیلی", "file_id": "BAACAgUAAxkBAAMcacguqtb1mWlIQ5Sy-wa6rjul5K8AAqgcAAIRfclVPSaCZvCnKcE6BA",
                 "caption": "✅ تحلیل تکنیکال و سبک‌های Price Action، RTM، ICT و Order Flow\n@cafetradetvaf"},
    "beg1_2_3": {"title": "جلسه سوم: اندیکاتورها و سیگنال‌ها", "file_id": "BAACAgUAAxkBAAMdacguqirEzGS62fnm7gssiHiQmP8AAn0hAALnm8hVCrd2Yn5-rdU6BA",
                 "caption": "✅ آشنایی با اندیکاتورها و سیگنال‌های معاملاتی\n@cafetradetvaf"},
    "beg1_2_4": {"title": "جلسه چهارم: تحلیل فاندامنتال", "file_id": "BAACAgUAAxkBAAMeacguqnoWSaUajxBjsw6kk4BQVSQAAkUaAAJE2SFW85cBSARvS5g6BA",
                 "caption": "✅ تحلیل اخبار اقتصادی و تاثیر آن بر بازار\n@cafetradetvaf"},
    "beg1_2_5": {"title": "جلسه پنجم: تعریف ساده داده‌ها", "file_id": "BAACAgUAAxkBAAMfacguqlSw53-PkJFbJk3uq4pHsnMAAjEaAAJE2SFWqxfcvUYgke46BA",
                 "caption": "✅ مفاهیم اقتصادی: نرخ بهره، تورم، سیاست‌های اقتصادی\n@cafetradetvaf"},
    # فصل دوم: پیشرفته - placeholder
    "beg2_1_1": {"title": "جلسه اول فصل دوم", "file_id": "PLACEHOLDER_FILE_ID_1", "caption": "کپشن جلسه اول فصل دوم\n@cafetradetvaf"},
    "beg2_1_2": {"title": "جلسه دوم فصل دوم", "file_id": "PLACEHOLDER_FILE_ID_2", "caption": "کپشن جلسه دوم فصل دوم\n@cafetradetvaf"},
}

menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2","beg1_1_3","beg1_1_4","beg1_1_5","beg1_1_6"],
        "بخش دوم: تحلیل بازار": ["beg1_2_1","beg1_2_2","beg1_2_3","beg1_2_4","beg1_2_5"],
    },
    "فصل دوم: پیشرفته": {
        "بخش اول: جلسات پیشرفته": ["beg2_1_1","beg2_1_2"]
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "intro":
        chat_id = query.message.chat_id
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=sessions["intro"]["file_id"], caption=sessions["intro"]["caption"])
        except TelegramError as e:
            logger.error(f"Failed to send intro video: {e}")
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup())
        return

    if data == "main":
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup())
        return

    # انتخاب فصل
    elif data.startswith("f"):
        f_number = data[1]
        if f_number == "1":
            buttons = [[InlineKeyboardButton(b, callback_data=f"f1_{i}")] for i, b in enumerate(menu_structure["فصل اول: ابتدایی"].keys())]
            buttons.append([InlineKeyboardButton("بازگشت", callback_data="main")])
            await query.message.edit_text("فصل اول: ابتدایی\nبخش مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        elif f_number == "2":
            buttons = [[InlineKeyboardButton(b, callback_data=f"f2_{i}")] for i, b in enumerate(menu_structure["فصل دوم: پیشرفته"].keys())]
            buttons.append([InlineKeyboardButton("بازگشت", callback_data="main")])
            await query.message.edit_text("فصل دوم: پیشرفته\nبخش مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await query.message.edit_text("این فصل فعلاً در دسترس نیست.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]]))
        return

    # انتخاب بخش فصل اول
    elif data.startswith("f1_"):
        idx = int(data.split("_")[1])
        section_name = list(menu_structure["فصل اول: ابتدایی"].keys())[idx]
        sessions_list = menu_structure["فصل اول: ابتدایی"][section_name]
        buttons = [[InlineKeyboardButton(sessions[s]["title"], callback_data=s)] for s in sessions_list]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="f1")])
        await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # انتخاب بخش فصل دوم
    elif data.startswith("f2_"):
        idx = int(data.split("_")[1])
        section_name = list(menu_structure["فصل دوم: پیشرفته"].keys())[idx]
        sessions_list = menu_structure["فصل دوم: پیشرفته"][section_name]
        buttons = [[InlineKeyboardButton(sessions[s]["title"], callback_data=s)] for s in sessions_list]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="f2")])
        await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # ارسال ویدیو
    elif data in sessions:
        s = sessions[data]
        chat_id = query.message.chat_id
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=s["file_id"], caption=s["caption"])
        except TelegramError as e:
            logger.error(f"Failed to send video for {data}: {e}")
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup())

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling update:", exc_info=context.error)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    print("Bot is running...")
    app.run_polling()