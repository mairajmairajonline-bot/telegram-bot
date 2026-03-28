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

sessions = {
    "intro": {"title": "معرفی دوره", "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA"},
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی", "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA"},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی", "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ"},
    "beg1_1_3": {"title": "جلسه سوم: تریدر کیست", "file_id": "BAACAgUAAxkBAAMXacguqjFHva0sNJqMQU823xJWsiAAAlEdAAK-qZhVfgocOT6_1gk6BA"},
    "beg1_1_4": {"title": "جلسه چهارم: انواع سبک‌های ترید", "file_id": "BAACAgUAAxkBAAMYacguqgFRh3FlotgC-HMkPimgGlwAAg8dAAIpZ7BVHnpO0EQ-0Jc6BA"},
    "beg1_1_5": {"title": "جلسه پنجم: نکات کلیدی برای شروع ترید", "file_id": "BAACAgUAAxkBAAMZacguqkRSe_qBmbMqVYFmLcwGHZ4AAkAeAAIaGrBVrvNEiiRia-A6BA"},
    "beg1_1_6": {"title": "جلسه ششم: خلاصه و جمع‌بندی", "file_id": "BAACAgUAAxkBAAMaacguqsV443jxKgTT3roWGBBeh8wAAlseAAIaGrBV6SJRv8Q1eDw6BA"},
    "beg1_2_1": {"title": "جلسه اول: آشنایی با تحلیل بازار", "file_id": "BAACAgUAAxkBAAMbacguqsR5nOj-1SOzWPiKE80uTLYAAjIcAAIRfclVy88EIhjFgDE6BA"},
    "beg1_2_2": {"title": "جلسه دوم: معرفی سبک‌های تحلیلی", "file_id": "BAACAgUAAxkBAAMcacguqtb1mWlIQ5Sy-wa6rjul5K8AAqgcAAIRfclVPSaCZvCnKcE6BA"},
    "beg1_2_3": {"title": "جلسه سوم: اندیکاتورها و سیگنال‌ها", "file_id": "BAACAgUAAxkBAAMdacguqirEzGS62fnm7gssiHiQmP8AAn0hAALnm8hVCrd2Yn5-rdU6BA"},
    "beg1_2_4": {"title": "جلسه چهارم: تحلیل فاندامنتال", "file_id": "BAACAgUAAxkBAAMeacguqnoWSaUajxBjsw6kk4BQVSQAAkUaAAJE2SFW85cBSARvS5g6BA"},
    "beg1_2_5": {"title": "جلسه پنجم: تعریف ساده داده‌ها", "file_id": "BAACAgUAAxkBAAMfacguqlSw53-PkJFbJk3uq4pHsnMAAjEaAAJE2SFWqxfcvUYgke46BA"},
}

menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2","beg1_1_3","beg1_1_4","beg1_1_5","beg1_1_6"],
        "بخش دوم: تحلیل بازار": ["beg1_2_1","beg1_2_2","beg1_2_3","beg1_2_4","beg1_2_5"],
    },
    "فصل دوم: پیشرفته": {},
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

    # ارسال ویدیو بدون تغییر پیام منو
    if data in sessions:
        s = sessions[data]
        chat_id = query.message.chat_id
        try:
            await context.bot.send_video(chat_id=chat_id, video=s["file_id"], caption=s["title"])
        except TelegramError as e:
            logger.error(f"Failed to send video for {data}: {e}")
            await context.bot.send_message(chat_id=chat_id, text=f"خطا در ارسال ویدیو:\n{e}")
        return

    # بازگشت به منوی اصلی
    if data == "main":
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup())
        return

    # معرفی دوره
    if data == "intro":
        chat_id = query.message.chat_id
        try:
            await context.bot.send_video(chat_id=chat_id, video=sessions["intro"]["file_id"], caption="معرفی دوره")
        except TelegramError as e:
            logger.error(f"Failed to send intro video: {e}")
            await context.bot.send_message(chat_id=chat_id, text=f"خطا در ارسال ویدیو:\n{e}")
        return

    # فصل اول
    if data == "f1":
        buttons = [[InlineKeyboardButton(b, callback_data=f"f1_{i}")] for i, b in enumerate(menu_structure["فصل اول: ابتدایی"].keys())]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="main")])
        await query.message.edit_text("فصل اول: ابتدایی\nبخش مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # فصل دوم و سوم
    if data in ("f2", "f3"):
        await query.message.edit_text(
            "این فصل فعلاً در دسترس نیست.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]])
        )
        return

    # بخش‌های فصل اول
    if "_" in data and data.startswith("f") and data[1].isdigit():
        f_key, idx = data.split("_", 1)
        idx = int(idx)
        if f_key == "f1":
            section_name = list(menu_structure["فصل اول: ابتدایی"].keys())[idx]
            sessions_list = menu_structure["فصل اول: ابتدایی"][section_name]
            buttons = [[InlineKeyboardButton(sessions[s]["title"], callback_data=s)] for s in sessions_list]
            buttons.append([InlineKeyboardButton("بازگشت", callback_data="f1")])
            await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

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