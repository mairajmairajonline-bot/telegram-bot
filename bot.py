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

# --- جلسات با کپشن کامل ---
sessions = {
    "intro": {"title": "معرفی دوره", "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA",
              "caption": "📚 آموزش بازار های مالی صفر تا صد:\n📚 معرفی دوره\n\n🔹در این ویدیو درباره شروع دوره و ساختار کامل کورس توضیح داده شده است.\nهمچنین با سرفصل‌ها و مراحل آموزشی دوره آشنا می‌شوید.\n\n@cafetradetvaf"},
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی",
                 "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه اول: تعریف ساده بازار های مالی\n\n✅ در این جلسه با تعریف ساده بازار، انواع بازارها، پیدایش و ضرورت بازارهای مالی و بسیاری موضوعات مهم دیگر آشنا می‌شوید.\n\n@cafetradetvaf"},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی",
                 "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه دوم: ماهیت بازار های مالی\n\n✅ در این جلسه انواع بازارهای مالی به‌صورت واضح و منظم توضیح داده شده و تمام جزئیات مربوط به انواع بازارهای مالی و مدیریت سرمایه مورد بحث قرار گرفته است.\n\n@cafetradetvaf"},
    "beg1_1_3": {"title": "جلسه سوم: تریدر کیست",
                 "file_id": "BAACAgUAAxkBAAMXacguqjFHva0sNJqMQU823xJWsiAAAlEdAAK-qZhVfgocOT6_1gk6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه سوم: تریدر کیست\n\n✅ در این جلسه ترید چیست ، تریدر کیست، سرمایه گذار کیست، تفاوت تریدر و سرمایه گذار تمام محتوا با جزییات ترتیب شده و خیلی مفصل و ساده بیان شده برای درک بهتر.\n\n@cafetradetvaf"},
    "beg1_1_4": {"title": "جلسه چهارم: انواع سبک‌های ترید",
                 "file_id": "BAACAgUAAxkBAAMYacguqgFRh3FlotgC-HMkPimgGlwAAg8dAAIpZ7BVHnpO0EQ-0Jc6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه چهارم: انواع سبک‌های ترید\n\n✅ در این جلسه با انواع روش‌های سرمایه‌گذاری و سبک‌های مختلف ترید مانند سویینگ تریدینگ، اسکالپینگ و دیتریدینگ آشنا می‌شوید و یاد می‌گیرید هر کدام چه ویژگی‌ها و کاربردی دارند.\n\n@cafetradetvaf"},
    "beg1_1_5": {"title": "جلسه پنجم: نکات کلیدی برای شروع ترید",
                 "file_id": "BAACAgUAAxkBAAMZacguqkRSe_qBmbMqVYFmLcwGHZ4AAkAeAAIaGrBVrvNEiiRia-A6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه پنجم: نکات کلیدی برای شروع ترید\n\n✅ در این جلسه بررسی می‌کنیم آیا می‌توان فقط روی ترید حساب کرد یا نه. همچنین با چند حقیقت مهم درباره بازارهای مالی آشنا می‌شویم و می‌فهمیم شروع ترید چقدر آسان یا چالش‌برانگیز است.\n\n@cafetradetvaf"},
    "beg1_1_6": {"title": "جلسه ششم: خلاصه و جمع‌بندی",
                 "file_id": "BAACAgUAAxkBAAMaacguqsV443jxKgTT3roWGBBeh8wAAlseAAIaGrBV6SJRv8Q1eDw6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه ششم: خلاصه و جمع بندی\n\n✅ در این جلسه یک مرور کوتاه و جمع‌بندی از تمام موضوعاتی که در جلسات قبلی گفته شد انجام می‌دهیم تا نکات مهم دوباره یادآوری و در ذهن شما تثبیت شود.\n\n@cafetradetvaf"},
    "beg1_2_1": {"title": "جلسه اول: آشنایی با تحلیل بازار",
                 "file_id": "BAACAgUAAxkBAAMbacguqsR5nOj-1SOzWPiKE80uTLYAAjIcAAIRfclVy88EIhjFgDE6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه اول: آشنایی با تحلیل بازار\n\n✅ در این جلسه با مفهوم تحلیل بازار آشنا می‌شویم، می‌فهمیم تحلیل بازار چیست، چرا برای معامله‌گران مهم است و چگونه کمک می‌کند تا زمان مناسب خرید، فروش یا صبر در بازارهای مالی را بهتر تشخیص دهیم.\n\n@cafetradetvaf"},
    "beg1_2_2": {"title": "جلسه دوم: معرفی سبک‌های تحلیلی",
                 "file_id": "BAACAgUAAxkBAAMcacguqtb1mWlIQ5Sy-wa6rjul5K8AAqgcAAIRfclVPSaCZvCnKcE6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه دوم: معرفی سبک های تحلیلی\n\n✅ در این جلسه با اهمیت تحلیل تکنیکال در معامله‌گری آشنا شویم و نگاهی کوتاه به سبک‌های مختلف آن مانند Price Action، RTM، ICT و Order Flow داشته باشیم تا بدانیم معامله‌گران با چه روش‌هایی بازار را تحلیل می‌کنند.\n\n@cafetradetvaf"},
    "beg1_2_3": {"title": "جلسه سوم: اندیکاتورها و سیگنال‌ها",
                 "file_id": "BAACAgUAAxkBAAMdacguqirEzGS62fnm7gssiHiQmP8AAn0hAALnm8hVCrd2Yn5-rdU6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه سوم: آشنایی با اندیکاتورها و سیگنال‌های معاملاتی\n\n✅ هدف این جلسه آشنایی با مفهوم اندیکاتورها و درک درست از سیگنال‌های معاملاتی است.\n\n@cafetradetvaf"},
    "beg1_2_4": {"title": "جلسه چهارم: تحلیل فاندامنتال",
                 "file_id": "BAACAgUAAxkBAAMeacguqnoWSaUajxBjsw6kk4BQVSQAAkUaAAJE2SFW85cBSARvS5g6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه چهارم: آشنایی با تحلیل فاندامنتال\n\n✅ هدف امروز این است که با مفهوم اخبار اقتصادی آشنا شویم، بفهمیم چرا این اخبار برای بازارهای مالی مهم هستند و چگونه معامله‌گران از آن‌ها برای تشخیص جهت بازار و کاهش ریسک استفاده می‌کنند.\n\n@cafetradetvaf"},
    "beg1_2_5": {"title": "جلسه پنجم: تعریف ساده داده‌ها",
                 "file_id": "BAACAgUAAxkBAAMfacguqlSw53-PkJFbJk3uq4pHsnMAAjEaAAJE2SFWqxfcvUYgke46BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه پنجم: تعریف ساده داده‌ها\n\n✅ هدف امروز این است که با مفاهیم مهم اقتصادی مانند نرخ بهره، تورم و سیاست‌های اقتصادی آشنا شویم و درک کنیم تصمیم‌های بانک مرکزی چگونه بر بازارهای مالی تأثیر می‌گذارند.\n\n@cafetradetvaf"},
}

# --- ساختار منو ---
menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2","beg1_1_3","beg1_1_4","beg1_1_5","beg1_1_6"],
        "بخش دوم: تحلیل بازار": ["beg1_2_1","beg1_2_2","beg1_2_3","beg1_2_4","beg1_2_5"],
    },
    "فصل دوم: پیشرفته": {},
    "فصل سوم: پروژه عملی": {}
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً فصل مورد نظر را انتخاب کنید:"

# --- ذخیره وضعیت کاربر ---
user_state = {}  # chat_id -> {"last_session": session_id}

# --- تابع ساخت دکمه‌ها ---
def build_buttons(items, chat_id=None, back_callback="main"):
    buttons = [[InlineKeyboardButton(item["title"] if isinstance(item, dict) else item, callback_data=item if isinstance(item, str) else item["callback"])] for item in items]
    # اضافه کردن دکمه ادامه آخرین جلسه
    if chat_id and chat_id in user_state and user_state[chat_id].get("last_session"):
        buttons.insert(0, [InlineKeyboardButton("🔄 ادامه آخرین جلسه", callback_data="last")])
    # دکمه برگشت
    buttons.append([InlineKeyboardButton("بازگشت", callback_data=back_callback)])
    return InlineKeyboardMarkup(buttons)

# --- هندلر استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MAIN_MENU_TEXT, reply_markup=build_buttons([
        {"title": "معرفی دوره", "callback": "intro"},
        {"title": "فصل اول: ابتدایی", "callback": "f1"},
        {"title": "فصل دوم: پیشرفته", "callback": "f2"},
        {"title": "فصل سوم: پروژه عملی", "callback": "f3"},
        {"title": "📋 جزئیات بیشتر", "callback": "link"}
    ], chat_id=update.message.chat_id))

# --- هندلر دکمه‌ها ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    # ادامه آخرین جلسه
    if data == "last" and chat_id in user_state and user_state[chat_id].get("last_session"):
        last = user_state[chat_id]["last_session"]
        await query.message.delete()
        await context.bot.send_video(chat_id=chat_id, video=sessions[last]["file_id"], caption=sessions[last]["caption"])
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # معرفی دوره
    if data == "intro":
        user_state[chat_id] = {"last_session": "intro"}
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=sessions["intro"]["file_id"], caption=sessions["intro"]["caption"])
        except TelegramError as e:
            logger.error(e)
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # بازگشت به منوی اصلی
    if data == "main":
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # لینک کانال
    if data == "link":
        await query.message.edit_text(f"📋 جزئیات بیشتر:\n{CHANNEL_LINK}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]]))
        return

    # انتخاب فصل
    if data.startswith("f"):
        f_key = "فصل اول: ابتدایی" if data=="f1" else "فصل دوم: پیشرفته" if data=="f2" else "فصل سوم: پروژه عملی"
        sections = list(menu_structure[f_key].keys())
        if not sections:
            await query.message.edit_text(f"{f_key}\n⚠️ این فصل هنوز آماده نشده و جلساتی ندارد.", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("بازگشت", callback_data="main")]
            ]))
            return
        buttons = [{"title": s, "callback": f"section_{f_key}_{i}"} for i,s in enumerate(sections)]
        await query.message.edit_text(f"{f_key}\nبخش مورد نظر را انتخاب کنید:", reply_markup=build_buttons(buttons, chat_id=chat_id, back_callback="main"))
        return

    # انتخاب بخش
    if data.startswith("section_"):
        _, f_key, idx = data.split("_")
        idx = int(idx)
        sections = list(menu_structure[f_key].keys())
        section_name = sections[idx]
        sessions_list = menu_structure[f_key][section_name]
        buttons = [{"title": sessions[s]["title"], "callback": s} for s in sessions_list]
        await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=build_buttons(buttons, chat_id=chat_id, back_callback="f1" if f_key=="فصل اول: ابتدایی" else "main"))
        return

    # انتخاب جلسه
    if data in sessions:
        user_state[chat_id] = {"last_session": data}
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=sessions[data]["file_id"], caption=sessions[data]["caption"])
        except TelegramError as e:
            logger.error(e)
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))

# --- منوی اصلی با دکمه ادامه آخرین جلسه ---
def main_menu_markup(chat_id=None):
    items = [
        {"title": "معرفی دوره", "callback": "intro"},
        {"title": "فصل اول: ابتدایی", "callback": "f1"},
        {"title": "فصل دوم: پیشرفته", "callback": "f2"},
        {"title": "فصل سوم: پروژه عملی", "callback": "f3"},
        {"title": "📋 جزئیات بیشتر", "callback": "link"}
    ]
    return build_buttons(items, chat_id=chat_id)

# --- هندلر خطا ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception:", exc_info=context.error)

# --- اجرا ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    print("Bot is running...")
    app.run_polling()