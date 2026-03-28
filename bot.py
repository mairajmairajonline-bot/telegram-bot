import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_LINK = "https://t.me/Amuzesh_cafetradeTvaf/84"

# --- دیتای کامل جلسات ---
sessions = {
    # فصل اول: ابتدایی / بخش اول: بازارهای مالی
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی", "file_id": "BAACAgUAAxkBAAPuacfeJowlwTSrzSQcSH4cp03A04EAAjgdAAK-qZhV9_r4GY2NUH86BA", "caption": "✅ در این جلسه با تعریف ساده بازار، انواع بازارها و پیدایش و ضرورت بازارهای مالی آشنا می‌شوید."},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی", "file_id": "BAACAgUAAxkBAAPvacfeJvopCeHdNwi6RB1HMcWKNUAAAkcdAAK-qZhVHBJzxt259_M6BA", "caption": "✅ در این جلسه انواع بازارهای مالی به‌صورت واضح و منظم توضیح داده شده است."},
    "beg1_1_3": {"title": "جلسه سوم: تریدر کیست", "file_id": "BAACAgUAAxkBAAPwacfeJgGVShPRmXLYSllvzu9MorkAAlEdAAK-qZhVBSYQlglskEA6BA", "caption": "✅ در این جلسه ترید چیست، تریدر کیست، سرمایه‌گذار کیست و تفاوت‌ها با جزئیات بیان شده."},
    "beg1_1_4": {"title": "جلسه چهارم: انواع سبک‌های ترید", "file_id": "BAACAgUAAxkBAAPxacfeJk0gzi3HtoMNYZcvdc_PhkkAAg8dAAIpZ7BVPQICGWRp5cI6BA", "caption": "✅ در این جلسه با انواع روش‌های سرمایه‌گذاری و سبک‌های مختلف ترید آشنا می‌شوید."},
    "beg1_1_5": {"title": "جلسه پنجم: نکات کلیدی برای شروع ترید", "file_id": "BAACAgUAAxkBAAPyacfeJv2SVuThPs-aOh93rR8ilcMAAkAeAAIaGrBVSNOcl6QpR_U6BA", "caption": "✅ در این جلسه بررسی می‌کنیم آیا می‌توان فقط روی ترید حساب کرد یا نه."},
    "beg1_1_6": {"title": "جلسه ششم: خلاصه و جمع‌بندی", "file_id": "BAACAgUAAxkBAAPzacfeJpwj2K8rodxFJPyn96aF__8AAlseAAIaGrBVATEiH7dULBo6BA", "caption": "✅ مرور کوتاه و جمع‌بندی از تمام موضوعات جلسات قبلی."},

    # فصل اول: ابتدایی / بخش دوم: تحلیل بازار
    "beg1_2_1": {"title": "جلسه اول: آشنایی با تحلیل بازار", "file_id": "BAACAgUAAxkBAAP0acfeJj-oHQXiQEnPbmY0AsHlUWgAAjIcAAIRfclVl_8FBMCEOEw6BA", "caption": "✅ در این جلسه با مفهوم تحلیل بازار آشنا می‌شویم و کاربرد آن در معامله‌گری."},
    "beg1_2_2": {"title": "جلسه دوم: معرفی سبک های تحلیلی", "file_id": "BAACAgUAAxkBAAP1acfeJgF1IyXGPerE5s_Dg4G3wm4AAqgcAAIRfclVG4nNE_pZ8t06BA", "caption": "✅ در این جلسه با سبک‌های مختلف تحلیل تکنیکال و اهمیت آن‌ها آشنا می‌شویم."},
    "beg1_2_3": {"title": "جلسه سوم: آشنایی با اندیکاتورها و سیگنال‌ها", "file_id": "BAACAgUAAxkBAAP2acfeJuFFQkzHcqxVg2DUcJSXex0AAn0hAALnm8hVcuduLufSx286BA", "caption": "✅ هدف این جلسه آشنایی با مفهوم اندیکاتورها و سیگنال‌های معاملاتی است."},
    "beg1_2_4": {"title": "جلسه چهارم: آشنایی با تحلیل فاندامنتال", "file_id": "BAACAgUAAxkBAAP3acfeJmGbWF7z66zey3Ddxo-nr_0AAkUaAAJE2SFWDsnyCuQAAaPMOgQ", "caption": "✅ هدف امروز آشنایی با اخبار اقتصادی و تحلیل فاندامنتال است."},
    "beg1_2_5": {"title": "جلسه پنجم: تعریف ساده داده ها", "file_id": "BAACAgUAAxkBAAPBacfM5RVkgHR88tDfRVWx1BiWqboAAjEaAAJE2SFWtEFJudqwyo46BA", "caption": "✅ در این جلسه با مفاهیم اقتصادی مهم مانند نرخ بهره، تورم و سیاست‌های اقتصادی آشنا می‌شویم."},

    # فصل اول: ابتدایی / بخش سوم: ابزار کاربردی
    "beg1_3_1": {"title": "جلسه اول: ابزار کاربردی ۱", "file_id": None, "caption": "این جلسه هنوز در دسترس نیست."},
    }

# --- استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("فصل اول: ابتدایی", callback_data="menu_beginner")],
        [InlineKeyboardButton("فصل دوم: پیشرفته", callback_data="menu_advanced")],
        [InlineKeyboardButton("فصل سوم: پروژه عملی", callback_data="menu_project")],
        [InlineKeyboardButton("📋 جزئیات بیشتر", url=CHANNEL_LINK)]
    ]
    await update.message.reply_text("📚 سیستم آموزش فعال شد\n\nیکی از گزینه‌ها را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))

# --- مدیریت دکمه‌ها ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_beginner":
        buttons = [
            [InlineKeyboardButton("بخش اول: بازارهای مالی", callback_data="menu_beg1_1")],
            [InlineKeyboardButton("بخش دوم: تحلیل بازار", callback_data="menu_beg1_2")],
            [InlineKeyboardButton("بخش سوم: ابزار کاربردی", callback_data="menu_beg1_3")],
            [InlineKeyboardButton("بازگشت", callback_data="back_main")],
            [InlineKeyboardButton("📋 جزئیات بیشتر", url=CHANNEL_LINK)]
        ]
        await query.message.edit_text("فصل اول: ابتدایی\nیک بخش را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("menu_beg1_"):
        section = data.split("_")[-1]
        section_sessions = {k: v for k, v in sessions.items() if k.startswith(f"beg1_{section}_")}
        buttons = [[InlineKeyboardButton(v["title"], callback_data=k)] for k, v in section_sessions.items()]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="menu_beginner")])
        buttons.append([InlineKeyboardButton("📋 جزئیات بیشتر", url=CHANNEL_LINK)])
        await query.message.edit_text(f"جلسات بخش {section}:", reply_markup=InlineKeyboardMarkup(buttons))

    elif data in sessions:
        session = sessions[data]
        if session["file_id"]:
            await query.message.reply_video(session["file_id"], caption=session["caption"])
        else:
            await query.message.reply_text(session["caption"])

    elif data == "back_main":
        await start(update, context)

    elif data == "menu_advanced":
        await query.message.reply_text("فصل دوم: پیشرفته - به زودی اضافه می‌شود.")

    elif data == "menu_project":
        await query.message.reply_text("فصل سوم: پروژه عملی - به زودی اضافه می‌شود.")

# --- اجرا ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
