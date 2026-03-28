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

# --- جلسات ---
sessions = {
    "intro": {"title": "معرفی دوره", "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA",
              "caption": "📚 معرفی دوره و ساختار آموزشی\n@cafetradetvaf"},
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی",
                 "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA",
                 "caption": "📚 فصل اول - بخش اول - جلسه اول\n@cafetradetvaf"},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی",
                 "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ",
                 "caption": "📚 فصل اول - بخش اول - جلسه دوم\n@cafetradetvaf"},
    # ... بقیه جلسات مثل قبل اضافه شود
}

# --- ساختار منو ---
menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2"],
        "بخش دوم: تحلیل بازار": [],
    },
    "فصل دوم: پیشرفته": {},
    "فصل سوم: پروژه عملی": {}
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً فصل مورد نظر را انتخاب کنید:"

# --- ذخیره وضعیت کاربر ---
user_state = {}  # chat_id -> {"last_session": session_id, "last_menu": menu_data}

# --- ساخت دکمه‌ها ---
def build_buttons(items, chat_id=None, back_callback="main"):
    buttons = [[InlineKeyboardButton(item["title"], callback_data=item["callback"])] for item in items]
    # اضافه کردن ادامه آخرین جلسه
    if chat_id and chat_id in user_state and user_state[chat_id].get("last_session"):
        buttons.insert(0, [InlineKeyboardButton("🔄 ادامه آخرین جلسه", callback_data="last")])
    # دکمه برگشت
    buttons.append([InlineKeyboardButton("بازگشت", callback_data=back_callback)])
    return InlineKeyboardMarkup(buttons)

# --- منوی اصلی ---
def main_menu_markup(chat_id=None):
    items = [
        {"title": "معرفی دوره", "callback": "intro"},
        {"title": "فصل اول: ابتدایی", "callback": "f1"},
        {"title": "فصل دوم: پیشرفته", "callback": "f2"},
        {"title": "فصل سوم: پروژه عملی", "callback": "f3"},
        {"title": "📋 جزئیات بیشتر", "callback": "link"}
    ]
    return build_buttons(items, chat_id=chat_id)

# --- هندلر استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in user_state:
        user_state[chat_id] = {"last_session": None, "last_menu": None}
    await update.message.reply_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))

# --- هندلر دکمه‌ها ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if chat_id not in user_state:
        user_state[chat_id] = {"last_session": None, "last_menu": None}

    # ادامه آخرین جلسه
    if data == "last" and user_state[chat_id]["last_session"]:
        last = user_state[chat_id]["last_session"]
        await query.message.delete()
        await context.bot.send_video(chat_id=chat_id, video=sessions[last]["file_id"], caption=sessions[last]["caption"])
        # بازگرداندن آخرین منو
        if user_state[chat_id]["last_menu"]:
            await query.message.reply_text(**user_state[chat_id]["last_menu"])
        else:
            await query.message.send_message(MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # لینک کانال
    if data == "link":
        await query.message.edit_text(f"📋 جزئیات بیشتر:\n{CHANNEL_LINK}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]]))
        return

    # بازگشت به منوی اصلی
    if data == "main":
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # معرفی دوره
    if data == "intro":
        user_state[chat_id]["last_session"] = "intro"
        user_state[chat_id]["last_menu"] = {"text": MAIN_MENU_TEXT, "reply_markup": main_menu_markup(chat_id)}
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=chat_id, video=sessions["intro"]["file_id"], caption=sessions["intro"]["caption"])
        except TelegramError as e:
            logger.error(e)
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))
        return

    # انتخاب فصل
    if data.startswith("f"):
        f_key = "فصل اول: ابتدایی" if data=="f1" else "فصل دوم: پیشرفته" if data=="f2" else "فصل سوم: پروژه عملی"
        sections = list(menu_structure[f_key].keys())
        if not sections:
            await query.message.edit_text(f"{f_key}\n⚠️ این فصل هنوز آماده نشده و جلساتی ندارد.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]]))
            return
        buttons = [{"title": s, "callback": f"section_{f_key}_{i}"} for i,s in enumerate(sections)]
        markup = build_buttons(buttons, chat_id=chat_id)
        user_state[chat_id]["last_menu"] = {"text": f"{f_key}\nبخش مورد نظر را انتخاب کنید:", "reply_markup": markup}
        await query.message.edit_text(f"{f_key}\nبخش مورد نظر را انتخاب کنید:", reply_markup=markup)
        return

    # انتخاب بخش
    if data.startswith("section_"):
        _, f_key, idx = data.split("_")
        idx = int(idx)
        sections = list(menu_structure[f_key].keys())
        section_name = sections[idx]
        sessions_list = menu_structure[f_key][section_name]
        buttons = [{"title": sessions[s]["title"], "callback": s} for s in sessions_list]
        markup = build_buttons(buttons, chat_id=chat_id, back_callback="f1" if f_key=="فصل اول: ابتدایی" else "main")
        user_state[chat_id]["last_menu"] = {"text": f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", "reply_markup": markup}
        await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=markup)
        return

    # انتخاب جلسه
    if data in sessions:
        user_state[chat_id]["last_session"] = data
        await query.message.delete()
        try:
            await context.bot.send_video(chat_id=chat_id, video=sessions[data]["file_id"], caption=sessions[data]["caption"])
        except TelegramError as e:
            logger.error(e)
        await context.bot.send_message(chat_id=chat_id, text=MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))

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