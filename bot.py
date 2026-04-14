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

# --- جلسات کامل ---
sessions = {
    "intro": {
        "title": "معرفی دوره",
        "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA",
        "caption": "📚 آموزش بازارهای مالی صفر تا صد\n📚 معرفی دوره\n\n🔹 ساختار کامل کورس و سرفصل‌ها توضیح داده شده.\n\n@cafetradetvaf"
    },

    "beg1_1_1": {
        "title": "جلسه اول: تعریف بازارهای مالی",
        "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA",
        "caption": "📊 تعریف ساده بازارهای مالی و انواع آن\n\n@cafetradetvaf"
    },

    "beg1_1_2": {
        "title": "جلسه دوم: ماهیت بازار",
        "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ",
        "caption": "📊 شناخت ماهیت بازارهای مالی\n\n@cafetradetvaf"
    },

    "beg1_2_1": {
        "title": "جلسه اول تحلیل بازار",
        "file_id": "BAACAgUAAxkBAAMbacguqsR5nOj-1SOzWPiKE80uTLYAAjIcAAIRfclVy88EIhjFgDE6BA",
        "caption": "📊 آشنایی با تحلیل بازار\n\n@cafetradetvaf"
    }
}

# --- لینک جزییات بیشتر ---
DETAILS_LINK = "https://t.me/Amuzesh_cafetradeTvaf/84"

menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1", "beg1_1_2"],
        "بخش دوم: تحلیل بازار": ["beg1_2_1"]
    }
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی\nانتخاب کنید:"

user_state = {}

# --- ساخت دکمه‌ها ---
def build_buttons(items, chat_id=None, back_callback=None):
    buttons = []

    for item in items:
        if item.get("type") == "url":
            buttons.append([InlineKeyboardButton(item["title"], url=item["url"])])
        else:
            buttons.append([InlineKeyboardButton(item["title"], callback_data=item["callback"])])

    if chat_id in user_state and user_state[chat_id].get("last_session"):
        buttons.insert(0, [InlineKeyboardButton("🔄 ادامه آخرین جلسه", callback_data="last")])

    if back_callback:
        buttons.append([InlineKeyboardButton("بازگشت", callback_data=back_callback)])

    return InlineKeyboardMarkup(buttons)

# --- منوی اصلی ---
def main_menu(chat_id):
    items = [
        {"title": "معرفی دوره", "callback": "intro"},
        {"title": "فصل اول: ابتدایی", "callback": "f1"},
        {"title": "جزییات بیشتر", "type": "url", "url": DETAILS_LINK}
    ]
    return MAIN_MENU_TEXT, build_buttons(items, chat_id)

# --- گرفتن منو ---
def get_menu(chat_id):
    state = user_state.get(chat_id, {})
    menu = state.get("menu", "main")

    if menu == "main":
        return main_menu(chat_id)

    if menu == "f1":
        items = [
            {"title": "بخش اول: بازارهای مالی", "callback": "section_1"},
            {"title": "بخش دوم: تحلیل بازار", "callback": "section_2"},
        ]
        return "فصل اول", build_buttons(items, chat_id, "main")

    if menu.startswith("section_"):
        if menu == "section_1":
            sess = menu_structure["فصل اول: ابتدایی"]["بخش اول: بازارهای مالی"]
        else:
            sess = menu_structure["فصل اول: ابتدایی"]["بخش دوم: تحلیل بازار"]

        items = [{"title": sessions[s]["title"], "callback": s} for s in sess]
        return "جلسات", build_buttons(items, chat_id, "f1")

    return main_menu(chat_id)

# --- ارسال منو ---
async def send_menu(context, chat_id):
    text, markup = get_menu(chat_id)

    old_msg = user_state.get(chat_id, {}).get("menu_msg_id")
    if old_msg:
        try:
            await context.bot.delete_message(chat_id, old_msg)
        except:
            pass

    msg = await context.bot.send_message(chat_id, text, reply_markup=markup)

    user_state.setdefault(chat_id, {})
    user_state[chat_id]["menu_msg_id"] = msg.message_id

# --- start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_state[chat_id] = {"menu": "main", "last_session": None}
    await send_menu(context, chat_id)

# --- button handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = query.message.chat_id

    user_state.setdefault(chat_id, {"menu": "main", "last_session": None})

    if data == "main":
        user_state[chat_id]["menu"] = "main"
        await send_menu(context, chat_id)
        return

    if data in ["f1", "section_1", "section_2"]:
        user_state[chat_id]["menu"] = data
        await send_menu(context, chat_id)
        return

    if data == "last":
        last = user_state[chat_id].get("last_session")
        if last:
            await context.bot.send_video(
                chat_id,
                sessions[last]["file_id"],
                caption=sessions[last]["caption"]
            )
        return

    if data in sessions:
        user_state[chat_id]["last_session"] = data
        await context.bot.send_video(
            chat_id,
            sessions[data]["file_id"],
            caption=sessions[data]["caption"]
        )
        await send_menu(context, chat_id)

# --- جلوگیری از پیام‌های کاربران (فقط ignore) ---
async def ignore_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return

# --- error ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error:", exc_info=context.error)

# --- run ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # فقط دکمه‌ها کار می‌کند، پیام‌ها نادیده گرفته می‌شوند
    app.add_handler(CommandHandler("message", ignore_messages))

    app.add_error_handler(error_handler)

    print("Bot Running...")
    app.run_polling()
