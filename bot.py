import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_LINK = "https://t.me/Amuzesh_cafetradeTvaf/84"
USER_STATE_FILE = "user_state.json"

# --- بارگذاری وضعیت کاربران ---
if os.path.exists(USER_STATE_FILE):
    with open(USER_STATE_FILE, "r", encoding="utf-8") as f:
        user_state = json.load(f)
else:
    user_state = {}

def save_state():
    with open(USER_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(user_state, f, ensure_ascii=False, indent=2)

# --- جلسات ---
sessions = {
    "intro": {"title": "معرفی دوره", "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA", "caption": "📚 معرفی دوره\n\n@cafetradetvaf"},
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی", "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه اول\n✅ توضیحات کامل\n@cafetradetvaf"},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی", "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه دوم\n✅ توضیحات کامل\n@cafetradetvaf"},
    "beg1_1_3": {"title": "جلسه سوم: تریدر کیست", "file_id": "BAACAgUAAxkBAAMXacguqjFHva0sNJqMQU823xJWsiAAAlEdAAK-qZhVfgocOT6_1gk6BA", "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه سوم\n✅ توضیحات کامل\n@cafetradetvaf"},
    # ... باقی جلسات فصل اول بخش اول و دوم مثل قبل
}

# --- ساختار منو ---
menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2","beg1_1_3"],
        # "بخش دوم: تحلیل بازار": ["beg1_2_1", ...] میتونی اضافه کنی
    },
    "فصل دوم: پیشرفته": {},
    "فصل سوم: پروژه عملی": {}
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً فصل مورد نظر را انتخاب کنید:"

def main_menu_markup(chat_id=None):
    buttons = [
        [InlineKeyboardButton("معرفی دوره", callback_data="intro")],
        [InlineKeyboardButton("فصل اول: ابتدایی", callback_data="f1")],
        [InlineKeyboardButton("فصل دوم: پیشرفته", callback_data="f2")],
        [InlineKeyboardButton("فصل سوم: پروژه عملی", callback_data="f3")],
        [InlineKeyboardButton("📋 جزئیات بیشتر", url=CHANNEL_LINK)]
    ]
    # اگر کاربر آخرین جلسه دارد، دکمه اضافه می‌کنیم
    if chat_id and chat_id in user_state and user_state[chat_id].get("last_session"):
        buttons.insert(0, [InlineKeyboardButton("🔄 ادامه آخرین جلسه", callback_data="last")])
    return InlineKeyboardMarkup(buttons)

# --- هندلر استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    await update.message.reply_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))

# --- هندلر دکمه‌ها ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = str(query.message.chat_id)
    chat_state = user_state.get(chat_id, {"last_session": None})

    # ادامه آخرین جلسه
    if data == "last":
        last = chat_state.get("last_session")
        if last and last in sessions:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=sessions[last]["file_id"], caption=sessions[last]["caption"])
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # معرفی دوره
    if data == "intro":
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=sessions["intro"]["file_id"], caption=sessions["intro"]["caption"])
            chat_state['last_session'] = "intro"
            user_state[chat_id] = chat_state
            save_state()
        except TelegramError as e:
            logger.error(e)
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # بازگشت به منوی اصلی
    if data == "main":
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # انتخاب فصل
    if data.startswith("f"):
        f_key = "فصل اول: ابتدایی" if data=="f1" else "فصل دوم: پیشرفته" if data=="f2" else "فصل سوم: پروژه عملی"
        sections = list(menu_structure[f_key].keys())
        if not sections:
            await query.message.edit_text(f"{f_key}\n⚠️ این فصل هنوز آماده نشده.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]]))
            return
        buttons = [[InlineKeyboardButton(s, callback_data=f"section_{f_key}_{i}")] for i,s in enumerate(sections)]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="main")])
        await query.message.edit_text(f"{f_key}\nبخش مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # انتخاب بخش
    if data.startswith("section_"):
        _, f_key, idx = data.split("_")
        idx = int(idx)
        sections = list(menu_structure[f_key].keys())
        section_name = sections[idx]
        sessions_list = menu_structure[f_key][section_name]
        buttons = [[InlineKeyboardButton(sessions[s]["title"], callback_data=s)] for s in sessions_list]
        buttons.append([InlineKeyboardButton("بازگشت", callback_data="f1" if f_key=="فصل اول: ابتدایی" else "main")])
        await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # انتخاب جلسه
    if data in sessions:
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=sessions[data]["file_id"], caption=sessions[data]["caption"])
            chat_state['last_session'] = data
            user_state[chat_id] = chat_state
            save_state()
        except TelegramError as e:
            logger.error(e)
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))

# --- هندلر خطا ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception:", exc_info=context.error)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    print("Bot is running...")
    app.run_polling()