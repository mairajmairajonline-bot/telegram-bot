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

# --- تمام جلسات فصل اول با کپشن کامل ---
sessions = {
    "intro": {"title": "معرفی دوره",
              "file_id": "BAACAgUAAxkBAAMUacguqjJioLir0_Slh2oxXeX7RtwAAikdAAK-qZhV4-NL-2f6R0Y6BA",
              "caption": "📚 آموزش بازارهای مالی صفر تا صد\n📚 معرفی دوره\n\n🔹در این ویدیو درباره شروع دوره و ساختار کامل کورس توضیح داده شده است.\nهمچنین با سرفصل‌ها و مراحل آموزشی دوره آشنا می‌شوید.\n\n@cafetradetvaf"},
    "beg1_1_1": {"title": "جلسه اول: تعریف ساده بازارهای مالی ",
                 "file_id": "BAACAgUAAxkBAAMVacguqsUgRSWfxHTBOKw25G7WGcUAAjgdAAK-qZhVBq6dWRpZJN46BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه اول: تعریف ساده بازارهای مالی\n\n✅ در این جلسه با تعریف ساده بازار، انواع بازارها، پیدایش و ضرورت بازارهای مالی و بسیاری موضوعات مهم دیگر آشنا می‌شوید.\n\n@cafetradetvaf"},
    "beg1_1_2": {"title": "جلسه دوم: ماهیت بازارهای مالی",
                 "file_id": "BAACAgUAAxkBAAMWacguqomeue1TnljEAAE32XUDcG-kAAJHHQACvqmYVZRdzsn-twr6OgQ",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه دوم: ماهیت بازارهای مالی\n\n✅ در این جلسه انواع بازارهای مالی به‌صورت واضح و منظم توضیح داده شده و تمام جزئیات مربوط به انواع بازارهای مالی و مدیریت سرمایه مورد بحث قرار گرفته است.\n\n@cafetradetvaf"},
    "beg1_1_3": {"title": "جلسه سوم: تریدر کیست",
                 "file_id": "BAACAgUAAxkBAAMXacguqjFHva0sNJqMQU823xJWsiAAAlEdAAK-qZhVfgocOT6_1gk6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه سوم: تریدر کیست\n\n✅ در این جلسه ترید چیست، تریدر کیست، سرمایه گذار کیست، تفاوت تریدر و سرمایه گذار تمام محتوا با جزییات ترتیب شده و خیلی مفصل بیان شده است.\n\n@cafetradetvaf"},
    "beg1_1_4": {"title": "جلسه چهارم: انواع سبک‌های ترید",
                 "file_id": "BAACAgUAAxkBAAMYacguqgFRh3FlotgC-HMkPimgGlwAAg8dAAIpZ7BVHnpO0EQ-0Jc6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه چهارم: انواع سبک‌های ترید\n\n✅ در این جلسه با انواع روش‌های سرمایه‌گذاری و سبک‌های مختلف ترید مانند سویینگ تریدینگ، اسکالپینگ و دیتریدینگ آشنا می‌شوید و ویژگی‌ها و کاربرد هر کدام را می‌آموزید.\n\n@cafetradetvaf"},
    "beg1_1_5": {"title": "جلسه پنجم: نکات کلیدی برای شروع ترید",
                 "file_id": "BAACAgUAAxkBAAMZacguqkRSe_qBmbMqVYFmLcwGHZ4AAkAeAAIaGrBVrvNEiiRia-A6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه پنجم: نکات کلیدی برای شروع ترید\n\n✅ در این جلسه بررسی می‌کنیم آیا می‌توان فقط روی ترید حساب کرد یا نه و با چند حقیقت مهم درباره بازارهای مالی آشنا می‌شویم.\n\n@cafetradetvaf"},
    "beg1_1_6": {"title": "جلسه ششم: خلاصه و جمع‌بندی",
                 "file_id": "BAACAgUAAxkBAAMaacguqsV443jxKgTT3roWGBBeh8wAAlseAAIaGrBV6SJRv8Q1eDw6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه ششم: خلاصه و جمع‌بندی\n\n✅ مرور کوتاه و جمع‌بندی از تمام موضوعات جلسات قبلی انجام شده تا نکات مهم تثبیت شوند.\n\n@cafetradetvaf"},
    # --- بخش دوم تحلیل بازار ---
    "beg1_2_1": {"title": "جلسه اول: آشنایی با تحلیل بازار",
                 "file_id": "BAACAgUAAxkBAAMbacguqsR5nOj-1SOzWPiKE80uTLYAAjIcAAIRfclVy88EIhjFgDE6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه اول: آشنایی با تحلیل بازار\n\n✅ با مفهوم تحلیل بازار، اهمیت آن و تشخیص زمان مناسب خرید و فروش آشنا می‌شویم.\n\n@cafetradetvaf"},
    "beg1_2_2": {"title": "جلسه دوم: معرفی سبک‌های تحلیلی",
                 "file_id": "BAACAgUAAxkBAAMcacguqtb1mWlIQ5Sy-wa6rjul5K8AAqgcAAIRfclVPSaCZvCnKcE6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه دوم: معرفی سبک‌های تحلیلی\n\n✅ اهمیت تحلیل تکنیکال و معرفی سبک‌هایی مانند Price Action، RTM، ICT و Order Flow.\n\n@cafetradetvaf"},
    "beg1_2_3": {"title": "جلسه سوم: اندیکاتورها و سیگنال‌ها",
                 "file_id": "BAACAgUAAxkBAAMdacguqirEzGS62fnm7gssiHiQmP8AAn0hAALnm8hVCrd2Yn5-rdU6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه سوم: آشنایی با اندیکاتورها و سیگنال‌ها\n\n✅ مفهوم اندیکاتورها و درک صحیح سیگنال‌های معاملاتی.\n\n@cafetradetvaf"},
    "beg1_2_4": {"title": "جلسه چهارم: تحلیل فاندامنتال",
                 "file_id": "BAACAgUAAxkBAAMeacguqnoWSaUajxBjsw6kk4BQVSQAAkUaAAJE2SFW85cBSARvS5g6BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه چهارم: تحلیل فاندامنتال\n\n✅ مفهوم اخبار اقتصادی و استفاده از آن‌ها برای پیش‌بینی بازار.\n\n@cafetradetvaf"},
    "beg1_2_5": {"title": "جلسه پنجم: تعریف ساده داده‌ها",
                 "file_id": "BAACAgUAAxkBAAMfacguqlSw53-PkJFbJk3uq4pHsnMAAjEaAAJE2SFWqxfcvUYgke46BA",
                 "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه پنجم: تعریف ساده داده‌ها\n\n✅ آشنایی با مفاهیم اقتصادی مهم مانند نرخ بهره، تورم و سیاست‌های اقتصادی و تاثیر آن‌ها بر بازار.\n\n@cafetradetvaf"},
    # --- جزییات بیشتر مستقیم لینک ---
    "details_more": {"title": "جزییات بیشتر", "link": "https://t.me/Amuzesh_cafetradeTvaf/84"}
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

# --- ساخت دکمه‌ها ---
def build_buttons(items, chat_id=None, back_callback=None):
    buttons = []
    for item in items:
        if 'callback' in item:
            buttons.append([InlineKeyboardButton(item["title"], callback_data=item["callback"])])
        elif 'link' in item:
            buttons.append([InlineKeyboardButton(item["title"], url=item["link"])])
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
        {"title": "جزییات بیشتر", "link": sessions['details_more']['link']}
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

    if data == "intro":
        user_state[chat_id]["last_session"] = "intro"
        await context.bot.send_video(chat_id=chat_id, video=sessions["intro"]["file_id"], caption=sessions["intro"]["caption"])
        await send_menu(context, chat_id)
        return

    if data == "last":
        last = user_state[chat_id].get("last_session")
        if last:
            await context.bot.send_video(chat_id=chat_id, video=sessions[last]["file_id"], caption=sessions[last]["caption"])
            await send_menu(context, chat_id)
        return

    if data in sessions and "file_id" in sessions[data]:
        user_state[chat_id]["last_session"] = data
        await context.bot.send_video(chat_id=chat_id, video=sessions[data]["file_id"], caption=sessions[data]["caption"])
        await send_menu(context, chat_id)
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
