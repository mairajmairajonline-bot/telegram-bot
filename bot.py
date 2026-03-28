import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# --- دیتای جلسات ---
sessions = {
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی", "file_id": "BAACAgUAAxkBAAPuacfeJowlwTSrzSQcSH4cp03A04EAAjgdAAK-qZhV9_r4GY2NUH86BA", "caption": "✅ در این جلسه با مفاهیم ابتدایی بازارهای مالی آشنا می‌شوید."},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی", "file_id": "BAACAgUAAxkBAAPvacfeJvopCeHdNwi6RB1HMcWKNUAAAkcdAAK-qZhVHBJzxt259_M6BA", "caption": "✅ در این جلسه ماهیت و انواع بازارهای مالی بررسی می‌شود."},

    "beg1_2_1": {"title": "جلسه اول: آشنایی با تحلیل بازار", "file_id": "BAACAgUAAxkBAAP0acfeJj-oHQXiQEnPbmY0AsHlUWgAAjIcAAIRfclVl_8FBMCEOEw6BA", "caption": "✅ در این جلسه با مفهوم تحلیل بازار آشنا می‌شوید."},

    "beg1_3_1": {"title": "جلسه اول: ابزارهای کاربردی", "file_id": None, "caption": "این جلسه در حال حاضر در دسترس نمی‌باشد."},
}

# --- استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("📘 فصل اول: سطح ابتدایی", callback_data="menu_beginner")],
        [InlineKeyboardButton("📗 فصل دوم: سطح پیشرفته", callback_data="menu_advanced")],
        [InlineKeyboardButton("🏁 فصل سوم: پروژه عملی", callback_data="menu_project")],
        [InlineKeyboardButton("📋 جزئیات بیشتر", callback_data="details_more")]
    ]

    await update.message.reply_text(
        "📚 سیستم آموزش بازارهای مالی فعال شد\n\nلطفاً یکی از فصل‌ها را انتخاب نمایید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- گرفتن file_id ---
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        await update.message.reply_text(update.message.video.file_id)

# --- مدیریت دکمه‌ها ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # فصل اول
    if data == "menu_beginner":
        buttons = [
            [InlineKeyboardButton("📊 بخش اول: بازارهای مالی", callback_data="menu_beg1_1")],
            [InlineKeyboardButton("📊 بخش دوم: تحلیل بازار", callback_data="menu_beg1_2")],
            [InlineKeyboardButton("📊 بخش سوم: ابزارهای کاربردی", callback_data="menu_beg1_3")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ]

        await query.message.edit_text(
            "📘 فصل اول: سطح ابتدایی\n\nلطفاً یکی از بخش‌ها را انتخاب نمایید:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # بخش‌ها → جلسات
    elif data.startswith("menu_beg1_"):
        section = data.split("_")[-1]
        section_sessions = {k: v for k, v in sessions.items() if k.startswith(f"beg1_{section}_")}

        buttons = [[InlineKeyboardButton(v["title"], callback_data=k)] for k, v in section_sessions.items()]
        buttons.append([InlineKeyboardButton("🔙 بازگشت", callback_data="menu_beginner")])

        await query.message.edit_text(
            "لطفاً جلسه مورد نظر خود را انتخاب نمایید:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # جلسات
    elif data in sessions:
        session = sessions[data]
        if session["file_id"]:
            await query.message.reply_video(session["file_id"], caption=session["caption"])
        else:
            await query.message.reply_text("این جلسه در حال حاضر در دسترس نمی‌باشد.")

    # بازگشت به منوی اصلی
    elif data == "back_main":
        await start(update, context)

    # فصل‌های دیگر
    elif data == "menu_advanced":
        await query.message.reply_text("📗 فصل پیشرفته به‌زودی در دسترس قرار خواهد گرفت.")

    elif data == "menu_project":
        await query.message.reply_text("🏁 فصل پروژه عملی به‌زودی اضافه خواهد شد.")

    # جزئیات بیشتر (بدون لینک)
    elif data == "details_more":
        await query.message.reply_text(
            "📌 جهت دریافت جزئیات کامل آموزش‌ها، لطفاً به کانال مراجعه نمایید."
        )

# --- اجرا ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO, get_file_id))
    app.run_polling()