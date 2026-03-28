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

# --- جلسات فصل اول با کپشن کامل و جزییات ---
sessions = {
    # معرفی دوره
    "intro": {
        "title": "معرفی دوره",
        "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA",
        "caption": "📚 آموزش بازار های مالی صفر تا صد:\n📚 معرفی دوره\n\n🔹در این ویدیو درباره شروع دوره و ساختار کامل کورس توضیح داده شده است.\nهمچنین با سرفصل‌ها و مراحل آموزشی دوره آشنا می‌شوید.\n\n@cafetradetvaf",
        "details": "در این ویدیو درباره ساختار کامل کورس، سرفصل‌ها و مراحل آموزشی توضیح داده شده است."
    },
    # بخش اول: بازارهای مالی
    "beg1_1_1": {
        "title": "جلسه اول: تعریف ساده بازارهای مالی",
        "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه اول: تعریف ساده بازار های مالی\n\n✅ در این جلسه با تعریف ساده بازار، انواع بازارها، پیدایش و ضرورت بازارهای مالی و بسیاری موضوعات مهم دیگر آشنا می‌شوید.\n\n@cafetradetvaf",
        "details": "در این جلسه با تعریف ساده بازار، انواع بازارها و ضرورت بازارهای مالی آشنا می‌شوید."
    },
    "beg1_1_2": {
        "title": "جلسه دوم: ماهیت بازارهای مالی",
        "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه دوم: ماهیت بازار های مالی\n\n✅ در این جلسه انواع بازارهای مالی به‌صورت واضح و منظم توضیح داده شده و تمام جزئیات مربوط به انواع بازارهای مالی و مدیریت سرمایه مورد بحث قرار گرفته است.\n\n@cafetradetvaf",
        "details": "در این جلسه انواع بازارهای مالی و مدیریت سرمایه به‌صورت کامل توضیح داده شده است."
    },
    "beg1_1_3": {
        "title": "جلسه سوم: تریدر کیست",
        "file_id": "BAACAgUAAxkBAAMXacguqjFHva0sNJqMQU823xJWsiAAAlEdAAK-qZhVfgocOT6_1gk6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه سوم: تریدر کیست\n\n✅ در این جلسه ترید چیست ، تریدر کیست، سرمایه گذار کیست، تفاوت تریدر و سرمایه گذار تمام محتوا با جزییات ترتیب شده و خیلی مفصل و ساده بیان شده برای درک بهتر.\n\n@cafetradetvaf",
        "details": "در این جلسه با مفاهیم تریدر و سرمایه‌گذار، تفاوت‌ها و نحوه فعالیت هر کدام آشنا می‌شوید."
    },
    "beg1_1_4": {
        "title": "جلسه چهارم: انواع سبک‌های ترید",
        "file_id": "BAACAgUAAxkBAAMYacguqgFRh3FlotgC-HMkPimgGlwAAg8dAAIpZ7BVHnpO0EQ-0Jc6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه چهارم: انواع سبک‌های ترید\n\n✅ در این جلسه با انواع روش‌های سرمایه‌گذاری و سبک‌های مختلف ترید مانند سویینگ تریدینگ، اسکالپینگ و دیتریدینگ آشنا می‌شوید و یاد می‌گیرید هر کدام چه ویژگی‌ها و کاربردی دارند.\n\n@cafetradetvaf",
        "details": "سبک‌های مختلف ترید و کاربرد هرکدام را به‌طور کامل بررسی می‌کنیم."
    },
    "beg1_1_5": {
        "title": "جلسه پنجم: نکات کلیدی برای شروع ترید",
        "file_id": "BAACAgUAAxkBAAMZacguqkRSe_qBmbMqVYFmLcwGHZ4AAkAeAAIaGrBVrvNEiiRia-A6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه پنجم: نکات کلیدی برای شروع ترید\n\n✅ در این جلسه بررسی می‌کنیم آیا می‌توان فقط روی ترید حساب کرد یا نه. همچنین با چند حقیقت مهم درباره بازارهای مالی آشنا می‌شویم و می‌فهمیم شروع ترید چقدر آسان یا چالش‌برانگیز است.\n\n@cafetradetvaf",
        "details": "نکات عملی و کلیدی برای شروع ترید و جلوگیری از اشتباهات رایج."
    },
    "beg1_1_6": {
        "title": "جلسه ششم: خلاصه و جمع‌بندی",
        "file_id": "BAACAgUAAxkBAAMaacguqsV443jxKgTT3roWGBBeh8wAAlseAAIaGrBV6SJRv8Q1eDw6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه ششم: خلاصه و جمع بندی\n\n✅ در این جلسه یک مرور کوتاه و جمع‌بندی از تمام موضوعاتی که در جلسات قبلی گفته شد انجام می‌دهیم تا نکات مهم دوباره یادآوری و در ذهن شما تثبیت شود.\n\n@cafetradetvaf",
        "details": "جمع‌بندی کلی و نکات مهم فصل اول برای تثبیت یادگیری."
    },
    # بخش دوم: تحلیل بازار
    "beg1_2_1": {
        "title": "جلسه اول: آشنایی با تحلیل بازار",
        "file_id": "BAACAgUAAxkBAAMbacguqsR5nOj-1SOzWPiKE80uTLYAAjIcAAIRfclVy88EIhjFgDE6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه اول: آشنایی با تحلیل بازار\n\n✅ در این جلسه با مفهوم تحلیل بازار آشنا می‌شویم و می‌فهمیم تحلیل بازار چیست و چرا برای معامله‌گران مهم است.\n\n@cafetradetvaf",
        "details": "مبانی تحلیل بازار و اهمیت آن در معاملات."
    },
    "beg1_2_2": {
        "title": "جلسه دوم: معرفی سبک‌های تحلیلی",
        "file_id": "BAACAgUAAxkBAAMcacguqtb1mWlIQ5Sy-wa6rjul5K8AAqgcAAIRfclVPSaCZvCnKcE6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه دوم: معرفی سبک‌های تحلیلی\n\n✅ در این جلسه با سبک‌های مختلف تحلیل تکنیکال و اهمیت آن‌ها آشنا می‌شویم.\n\n@cafetradetvaf",
        "details": "مروری بر Price Action، RTM، ICT و Order Flow و کاربرد آن‌ها."
    },
    "beg1_2_3": {
        "title": "جلسه سوم: اندیکاتورها و سیگنال‌ها",
        "file_id": "BAACAgUAAxkBAAMdacguqirEzGS62fnm7gssiHiQmP8AAn0hAALnm8hVCrd2Yn5-rdU6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه سوم: اندیکاتورها و سیگنال‌ها\n\n✅ هدف این جلسه آشنایی با اندیکاتورها و سیگنال‌های معاملاتی است.\n\n@cafetradetvaf",
        "details": "مفهوم اندیکاتورها و نحوه استفاده از سیگنال‌ها."
    },
    "beg1_2_4": {
        "title": "جلسه چهارم: تحلیل فاندامنتال",
        "file_id": "BAACAgUAAxkBAAMeacguqnoWSaUajxBjsw6kk4BQVSQAAkUaAAJE2SFW85cBSARvS5g6BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه چهارم: تحلیل فاندامنتال\n\n✅ با اخبار اقتصادی و تاثیر آن‌ها بر بازارهای مالی آشنا می‌شویم.\n\n@cafetradetvaf",
        "details": "مفهوم اخبار اقتصادی و کاربرد آن در کاهش ریسک معاملات."
    },
    "beg1_2_5": {
        "title": "جلسه پنجم: تعریف ساده داده‌ها",
        "file_id": "BAACAgUAAxkBAAMfacguqlSw53-PkJFbJk3uq4pHsnMAAjEaAAJE2SFWqxfcvUYgke46BA",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه پنجم: تعریف ساده داده‌ها\n\n✅ آشنایی با مفاهیم اقتصادی مهم و تاثیر آن‌ها بر بازارهای مالی.\n\n@cafetradetvaf",
        "details": "نرخ بهره، تورم و سیاست‌های اقتصادی و تاثیر آن بر بازار."
    },
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

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً انتخاب کنید:"
user_state = {}

# --- ساخت دکمه‌ها با گزینه جزییات بیشتر ---
def build_buttons(items, chat_id=None, back_callback=None):
    buttons = []
    for item in items:
        row = [InlineKeyboardButton(item["title"], callback_data=item["callback"])]
        if item["callback"] in sessions:
            row.append(InlineKeyboardButton("جزییات بیشتر", callback_data=f"details_{item['callback']}"))
        buttons.append(row)
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
        {"title": "فصل دوم: پیشرفته", "callback": "f2"},
        {"title": "فصل سوم: پروژه عملی", "callback": "f3"},
    ]
    return MAIN_MENU_TEXT, build_buttons(items, chat_id)

# --- گرفتن منو بر اساس وضعیت ---
def get_menu(chat_id):
    state = user_state.get(chat_id, {})
    menu = state.get("menu", "main")

    if menu == "main":
        return main_menu(chat_id)

    if menu.startswith("f"):
        f_key = "فصل اول: ابتدایی" if menu=="f1" else "فصل دوم: پیشرفته" if menu=="f2" else "فصل سوم: پروژه عملی"
        sections = list(menu_structure[f_key].keys())
        if not sections:
            return f"{f_key}\n⚠️ هنوز آماده نیست", InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]])
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

# --- ارسال منو ---
async def send_menu(context, chat_id):
    text, markup = get_menu(chat_id)
    old_msg_id = user_state.get(chat_id, {}).get("menu_msg_id")
    if old_msg_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except:
            pass
    msg = await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["menu_msg_id"] = msg.message_id

# --- ارسال جزییات بیشتر ---
async def send_details(context, chat_id, session_key):
    if session_key in sessions and "details" in sessions[session_key]:
        await context.bot.send_message(chat_id=chat_id, text=f"ℹ️ جزییات بیشتر درباره {sessions[session_key]['title']}:\n\n{sessions[session_key]['details']}")

# --- استارت ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_state[chat_id] = {"last_session": None, "menu": "main", "menu_msg_id": None}
    await send_menu(context, chat_id)

# --- هندلر دکمه‌ها ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if chat_id not in user_state:
        user_state[chat_id] = {"last_session": None, "menu": "main", "menu_msg_id": None}

    if data == "main":
        user_state[chat_id]["menu"] = "main"
        await send_menu(context, chat_id)
        return

    if data.startswith("f") or data.startswith("section_"):
        user_state[chat_id]["menu"] = data
        await send_menu(context, chat_id)
        return

    if data == "intro" or data in sessions:
        key = data
        user_state[chat_id]["last_session"] = key
        await context.bot.send_video(chat_id=chat_id, video=sessions[key]["file_id"], caption=sessions[key]["caption"])
        await send_menu(context, chat_id)
        return

    if data == "last":
        last = user_state[chat_id].get("last_session")
        if last:
            await context.bot.send_video(chat_id=chat_id, video=sessions[last]["file_id"], caption=sessions[last]["caption"])
            await send_menu(context, chat_id)
        return

    if data.startswith("details_"):
        session_key = data.split("_", 1)[1]
        await send_details(context, chat_id, session_key)
        return

# --- هندلر خطا ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error:", exc_info=context.error)

# --- اجرا ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    print("Bot Running...")
    app.run_polling()