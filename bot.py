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
    "intro": {"title": "معرفی دوره", "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA",
              "caption": "📚 معرفی دوره\n@cafetradetvaf"},
    "beg1_1_1": {"title": "جلسه اول", "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA",
                 "caption": "📚 جلسه اول\n@cafetradetvaf"},
    "beg1_1_2": {"title": "جلسه دوم", "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ",
                 "caption": "📚 جلسه دوم\n@cafetradetvaf"},
}

menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1","beg1_1_2"],
        "بخش دوم: تحلیل بازار": [],
    },
    "فصل دوم: پیشرفته": {},
    "فصل سوم: پروژه عملی": {}
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً انتخاب کنید:"

user_state = {}

def build_buttons(items, chat_id=None, back_callback="main"):
    buttons = [[InlineKeyboardButton(item["title"], callback_data=item["callback"])] for item in items]
    if chat_id in user_state and user_state[chat_id].get("last_session"):
        buttons.insert(0, [InlineKeyboardButton("🔄 ادامه آخرین جلسه", callback_data="last")])
    buttons.append([InlineKeyboardButton("بازگشت", callback_data=back_callback)])
    return InlineKeyboardMarkup(buttons)

def main_menu(chat_id):
    items = [
        {"title": "معرفی دوره", "callback": "intro"},
        {"title": "فصل اول: ابتدایی", "callback": "f1"},
        {"title": "فصل دوم: پیشرفته", "callback": "f2"},
        {"title": "فصل سوم: پروژه عملی", "callback": "f3"},
    ]
    return MAIN_MENU_TEXT, build_buttons(items, chat_id)

def get_menu(chat_id):
    state = user_state.get(chat_id, {})
    menu = state.get("menu", "main")

    if menu == "main":
        return main_menu(chat_id)

    if menu.startswith("f"):
        f_key = "فصل اول: ابتدایی" if menu=="f1" else "فصل دوم: پیشرفته" if menu=="f2" else "فصل سوم: پروژه عملی"
        sections = list(menu_structure[f_key].keys())

        if not sections:
            return f"{f_key}\n⚠️ آماده نیست", InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]])

        items = [{"title": s, "callback": f"section_{f_key}_{i}"} for i,s in enumerate(sections)]
        return f"{f_key}", build_buttons(items, chat_id, "main")

    if menu.startswith("section_"):
        _, f_key, idx = menu.split("_")
        idx = int(idx)
        sections = list(menu_structure[f_key].keys())
        section_name = sections[idx]
        sess = menu_structure[f_key][section_name]

        items = [{"title": sessions[s]["title"], "callback": s} for s in sess]
        return section_name, build_buttons(items, chat_id, "f1")

    return main_menu(chat_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_state[chat_id] = {"last_session": None, "menu": "main"}
    text, markup = main_menu(chat_id)
    await update.message.reply_text(text, reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if chat_id not in user_state:
        user_state[chat_id] = {"last_session": None, "menu": "main"}

    if data == "main":
        user_state[chat_id]["menu"] = "main"
        text, markup = main_menu(chat_id)
        await query.message.edit_text(text, reply_markup=markup)
        return

    if data.startswith("f"):
        user_state[chat_id]["menu"] = data
        text, markup = get_menu(chat_id)
        await query.message.edit_text(text, reply_markup=markup)
        return

    if data.startswith("section_"):
        user_state[chat_id]["menu"] = data
        text, markup = get_menu(chat_id)
        await query.message.edit_text(text, reply_markup=markup)
        return

    if data == "intro":
        user_state[chat_id]["last_session"] = "intro"
        await context.bot.send_video(chat_id=chat_id, video=sessions["intro"]["file_id"], caption=sessions["intro"]["caption"])
        text, markup = get_menu(chat_id)
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        return

    if data == "last":
        last = user_state[chat_id].get("last_session")
        if last:
            await context.bot.send_video(chat_id=chat_id, video=sessions[last]["file_id"], caption=sessions[last]["caption"])
            text, markup = get_menu(chat_id)
            await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        return

    if data in sessions:
        user_state[chat_id]["last_session"] = data
        await context.bot.send_video(chat_id=chat_id, video=sessions[data]["file_id"], caption=sessions[data]["caption"])
        text, markup = get_menu(chat_id)
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        return

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error:", exc_info=context.error)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    print("Bot Running...")
    app.run_polling()