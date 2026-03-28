import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

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
}

menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2"],
        "بخش دوم: تحلیل بازار": [],
    },
    "فصل دوم: پیشرفته": {},
    "فصل سوم: پروژه عملی": {}
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً فصل مورد نظر را انتخاب کنید:"

# ذخیره وضعیت کاربر
user_state = {}  # chat_id -> {"last_session": session_id, "last_menu_data": {"text":..., "markup":...}}

def build_buttons(items, chat_id=None, back_callback="main"):
    buttons = [[InlineKeyboardButton(item["title"], callback_data=item["callback"])] for item in items]
    # دکمه برگشت
    buttons.append([InlineKeyboardButton("بازگشت", callback_data=back_callback)])
    return InlineKeyboardMarkup(buttons)

def main_menu_markup(chat_id=None):
    items = [
        {"title": "معرفی دوره", "callback": "intro"},
        {"title": "فصل اول: ابتدایی", "callback": "f1"},
        {"title": "فصل دوم: پیشرفته", "callback": "f2"},
        {"title": "فصل سوم: پروژه عملی", "callback": "f3"},
        {"title": "📋 جزئیات بیشتر", "callback": "link"}
    ]
    return build_buttons(items, chat_id=chat_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in user_state:
        user_state[chat_id] = {"last_session": None, "last_menu_data": None}
    # اگر کاربر قبل هم منو رو باز کرده، همون وضعیت آخر رو نشون بده
    if user_state[chat_id]["last_menu_data"]:
        data = user_state[chat_id]["last_menu_data"]
        await update.message.reply_text(data["text"], reply_markup=data["markup"])
    else:
        await update.message.reply_text(MAIN_MENU_TEXT, reply_markup=main_menu_markup(chat_id))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if chat_id not in user_state:
        user_state[chat_id] = {"last_session": None, "last_menu_data": None}

    # لینک کانال
    if data == "link":
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]])
        user_state[chat_id]["last_menu_data"] = {"text": f"📋 جزئیات بیشتر:\n{CHANNEL_LINK}", "markup": markup}
        await query.message.edit_text(f"📋 جزئیات بیشتر:\n{CHANNEL_LINK}", reply_markup=markup)
        return

    # بازگشت به منوی اصلی
    if data == "main":
        markup = main_menu_markup(chat_id)
        user_state[chat_id]["last_menu_data"] = {"text": MAIN_MENU_TEXT, "markup": markup}
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=markup)
        return

    # معرفی دوره
    if data == "intro":
        user_state[chat_id]["last_session"] = "intro"
        markup = main_menu_markup(chat_id)
        user_state[chat_id]["last_menu_data"] = {"text": MAIN_MENU_TEXT, "markup": markup}
        await query.message.edit_text(MAIN_MENU_TEXT, reply_markup=markup)
        return

    # انتخاب فصل
    if data.startswith("f"):
        f_key = "فصل اول: ابتدایی" if data=="f1" else "فصل دوم: پیشرفته" if data=="f2" else "فصل سوم: پروژه عملی"
        sections = list(menu_structure[f_key].keys())
        if not sections:
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]])
            user_state[chat_id]["last_menu_data"] = {"text": f"{f_key}\n⚠️ این فصل هنوز آماده نشده و جلساتی ندارد.", "markup": markup}
            await query.message.edit_text(f"{f_key}\n⚠️ این فصل هنوز آماده نشده و جلساتی ندارد.", reply_markup=markup)
            return
        buttons = [{"title": s, "callback": f"section_{f_key}_{i}"} for i,s in enumerate(sections)]
        markup = build_buttons(buttons, chat_id=chat_id)
        user_state[chat_id]["last_menu_data"] = {"text": f"{f_key}\nبخش مورد نظر را انتخاب کنید:", "markup": markup}
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
        user_state[chat_id]["last_menu_data"] = {"text": f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", "markup": markup}
        await query.message.edit_text(f"{section_name}\nجلسه مورد نظر را انتخاب کنید:", reply_markup=markup)
        return

    # انتخاب جلسه
    if data in sessions:
        # فقط وضعیت ذخیره میشه، هیچ پیام یا ویدیویی فرستاده نمیشه
        user_state[chat_id]["last_session"] = data
        await query.message.edit_text(f"جلسه انتخاب شد: {sessions[data]['title']}", reply_markup=user_state[chat_id]["last_menu_data"]["markup"])

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()