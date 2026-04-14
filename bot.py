import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

sessions = {
    "intro": {
        "title": "معرفی دوره",
        "file_id": "BAACAgUAAxkDAAICMWnWpHC3ovu-Ztldc4jJvhu8bC-RAAIpHQACvqmYVePjS_tn-kdGOwQ",
        "caption": "📚 آموزش بازارهای مالی صفر تا صد\n📚 معرفی دوره\n\n🔹در این ویدیو درباره شروع دوره و ساختار کامل کورس توضیح داده شده است.\nهمچنین با سرفصل‌ها و مراحل آموزشی دوره آشنا می‌شوید.\n\n@cafetradetvaf"
    },

    # بخش اول: بازارهای مالی
    "beg1_1_1": {
        "title": "جلسه اول: تعریف ساده بازارهای مالی",
        "file_id": "BAACAgUAAxkDAAICSWneuRN69i13pNmS2zQlBkhPluePAAI4HQACvqmYVQaunVkaWSTeOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه اول: تعریف ساده بازار های مالی\n\n✅ در این جلسه با تعریف ساده بازار، انواع بازارها، پیدایش و ضرورت بازارهای مالی و بسیاری موضوعات مهم دیگر آشنا می‌شوید.\n\n@cafetradetvaf"
    },
    "beg1_1_2": {
        "title": "جلسه دوم: ماهیت بازارهای مالی",
        "file_id": "BAACAgUAAxkDAAICXGnevDW7Ouv_ZjhJfVsEuJQQ5zrvAAJHHQACvqmYVZRdzsn-twr6OwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه دوم: ماهیت بازار های مالی\n\n✅ در این جلسه انواع بازارهای مالی به‌صورت واضح و منظم توضیح داده شده و تمام جزئیات مربوط به انواع بازارهای مالی و مدیریت سرمایه مورد بحث قرار گرفته است.\n\n@cafetradetvaf"
    },
    "beg1_1_3": {
        "title": "جلسه سوم: تریدر کیست",
        "file_id": "BAACAgUAAxkBAAICg2nexVR6BaZZQhXPoVNDDnf2Hs8cAAJRHQACvqmYVX4KHDk-v9YJOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه سوم: تریدر کیست\n\n✅ در این جلسه ترید چیست، تریدر کیست، سرمایه گذار کیست، تفاوت تریدر و سرمایه گذار تمام محتوا با جزییات ترتیب شده و خیلی مفصل بیان شده است.\n\n@cafetradetvaf"
    },
    "beg1_1_4": {
        "title": "جلسه چهارم: انواع سبک‌های ترید",
        "file_id": "BAACAgUAAxkBAAIChGnexVSnr4Z4c9Oj8IZ29_OuFU6nAAIPHQACKWewVR56TtBEPtCXOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه چهارم: انواع سبک‌های ترید\n\n✅ در این جلسه با انواع روش‌های سرمایه‌گذاری و سبک‌های مختلف ترید مانند سویینگ تریدینگ، اسکالپینگ و دیتریدینگ آشنا می‌شوید و ویژگی‌ها و کاربرد هر کدام را می‌آموزید.\n\n@cafetradetvaf"
    },
    "beg1_1_5": {
        "title": "جلسه پنجم: نکات کلیدی برای شروع ترید",
        "file_id": "BAACAgUAAxkBAAIChWnexVQDwshBdu4HDHp41SvK6LFsAAJAHgACGhqwVa7zRIokYmvgOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه پنجم: نکات کلیدی برای شروع ترید\n\n✅ در این جلسه بررسی می‌کنیم آیا می‌توان فقط روی ترید حساب کرد یا نه و با چند حقیقت مهم درباره بازارهای مالی آشنا می‌شویم.\n\n@cafetradetvaf"
    },
    "beg1_1_6": {
        "title": "جلسه ششم: خلاصه و جمع‌بندی",
        "file_id": "BAACAgUAAxkDAAICQ2netm7_SsoFVUQhhAnBuKculmK6AAJbHgACGhqwVekiUb_ENXg8OwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش اول: بازارهای مالی\n🎓 جلسه ششم: خلاصه و جمع‌بندی\n\n✅ مرور کوتاه و جمع‌بندی از تمام موضوعات جلسات قبلی انجام شده تا نکات مهم تثبیت شوند.\n\n@cafetradetvaf"
    },

    # بخش دوم: تحلیل بازار
    "beg1_2_1": {
        "title": "جلسه اول: آشنایی با تحلیل بازار",
        "file_id": "BAACAgUAAxkBAAICh2nexVRT6lzKqqsr4O_9gB75ooGYAAIyHAACEX3JVcvPBCIYxYAxOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه اول: آشنایی با تحلیل بازار\n\n✅ در این جلسه با مفهوم تحلیل بازار آشنا می‌شویم، می‌فهمیم تحلیل بازار چیست، چرا برای معامله‌گران مهم است و چگونه کمک می‌کند تا زمان مناسب خرید، فروش یا صبر در بازارهای مالی را بهتر تشخیص دهیم.\n\n@cafetradetvaf"
    },
    "beg1_2_2": {
        "title": "جلسه دوم: معرفی سبک‌های تحلیلی",
        "file_id": "BAACAgUAAxkDAAICU2neu-IbiIjdnY1uRJlm2jff4japAAKoHAACEX3JVT0mgmbwpynBOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه دوم: معرفی سبک‌های تحلیلی\n\n✅ در این جلسه با اهمیت تحلیل تکنیکال در معامله‌گری آشنا شویم و نگاهی کوتاه به سبک‌های مختلف آن مانند Price Action، RTM، ICT و Order Flow داشته باشیم.\n\n@cafetradetvaf"
    },
    "beg1_2_3": {
        "title": "جلسه سوم: اندیکاتورها و سیگنال‌ها",
        "file_id": "BAACAgUAAxkBAAICiWnexVTzEq7UOe3r8nXru3qgX1IcAAJ9IQAC55vIVQq3dmJ-fq3VOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه سوم: آشنایی با اندیکاتورها و سیگنال‌های معاملاتی\n\n✅ هدف این جلسه آشنایی با مفهوم اندیکاتورها، نقش آن‌ها در تحلیل تکنیکال و همچنین درک درست از سیگنال‌های معاملاتی است.\n\n@cafetradetvaf"
    },
    "beg1_2_4": {
        "title": "جلسه چهارم: تحلیل فاندامنتال",
        "file_id": "BAACAgUAAxkBAAICimnexVSNRbQpZT_QYsUllvNxio4fAAJFGgACRNkhVvOXAUgEb0uYOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه چهارم: آشنایی با تحلیل فاندامنتال\n\n✅ هدف امروز این است که با مفهوم اخبار اقتصادی آشنا شویم، بفهمیم چرا این اخبار برای بازارهای مالی مهم هستند و چگونه معامله‌گران از آن‌ها برای تشخیص جهت بازار استفاده می‌کنند.\n\n@cafetradetvaf"
    },
    "beg1_2_5": {
        "title": "جلسه پنجم: تعریف ساده داده‌ها",
        "file_id": "BAACAgUAAxkDAAICcmnevkMDphtzqTWXfF1zNpWpTdz-AAIxGgACRNkhVqsX3L1GIJHuOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه پنجم: تعریف ساده داده‌ها\n\n✅ هدف امروز این است که با مفاهیم مهم اقتصادی مانند نرخ بهره، تورم و سیاست‌های اقتصادی آشنا شویم و درک کنیم تصمیم‌های بانک مرکزی چگونه بر بازارهای مالی تأثیر می‌گذارند.\n\n@cafetradetvaf"
    },
    "beg1_2_6": {
        "title": "جلسه ششم: سشن‌های معاملاتی",
        "file_id": "BAACAgUAAxkBAAICjGnexVQ55JZBSq5X2kj8EwQC6ykmAAKqGgACRNkhVmUhwqxfEbKbOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش دوم: تحلیل بازار\n🎓 جلسه ششم: سشن‌های معاملاتی\n\n✅ در این جلسه با مفهوم سشن معاملاتی آشنا می‌شویم، بدانیم هر سشن چه ویژگی‌هایی دارد و چطور شناخت سشن‌ها به معامله‌گر کمک می‌کند زمان مناسب معامله را انتخاب کند.\n\n@cafetradetvaf"
    },

    # بخش سوم: ابزار کاربردی
    "beg1_3_1": {
        "title": "جلسه اول: آشنایی با ابزار کاربردی",
        "file_id": "BAACAgUAAxkBAAICjWnexVR5pxsPVidgbDp3qGuks5JJAALPJgACr5lZVjanZqOOPH3ROwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه اول: آشنایی با ابزار کاربردی\n\n✅ در این جلسه با ستاپ پایه ترید آشنا می‌شویم، ابزارهای فیزیکی و نرم‌افزاری را می‌شناسیم و یاد می‌گیریم چرا مهارت‌ها و مدیریت سرمایه برای موفقیت در معامله ضروری است.\n\n@cafetradetvaf"
    },
    "beg1_3_2": {
        "title": "جلسه دوم: آموزش مولتی تایم فریم‌ها",
        "file_id": "BAACAgUAAxkBAAICjmnexVRKkU-eu14kGXNcH79wYMmOAALKHQAC1EthVpTu_RusReGIOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه دوم: آموزش مولتی تایم فریم‌ها\n\n✅ در این جلسه با مفهوم مولتی تایم‌فریم آشنا می‌شویم، یاد می‌گیریم چگونه بازار را در چند تایم‌فریم مختلف بررسی کنیم تا تحلیل دقیق‌تری داشته باشیم.\n\n@cafetradetvaf"
    },
    "beg1_3_3": {
        "title": "جلسه سوم: نحوه استفاده TradingView",
        "file_id": "BAACAgUAAxkBAAICj2nexVTonjdaqifCgH5zIo7d3K1eAAIrHwACFXt4ViFoPuUVPDhrOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه سوم: نحوه استفاده TradingView\n\n✅ در این جلسه با محیط TradingView آشنا می‌شویم، بخش‌های مختلف آن را می‌شناسیم و یاد می‌گیریم چگونه به‌صورت ساده از چارت‌ها استفاده کنیم تا تحلیل خود را شروع کنیم.\n\n@cafetradetvaf"
    },
    "beg1_3_4a": {
        "title": "جلسه چهارم: لوازم مورد نیاز ترید (قسمت اول)",
        "file_id": "BAACAgUAAxkBAAICkGnexVTp9eUg2OipC1epodG8OOMxAAIZHwACEHh5VjmxmGD7sW0ROwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه چهارم: لوازم مورد نیاز ترید\n🔘قسمت اول\n\n✅ در این جلسه یاد می‌گیریم چطور اطلاعات و اخبار بازار را جمع‌آوری و فیلتر کنیم، با سایت‌های مهم اقتصادی و تحلیلی آشنا می‌شویم.\n\n@cafetradetvaf"
    },
    "beg1_3_4b": {
        "title": "جلسه چهارم: لوازم مورد نیاز ترید (قسمت دوم)",
        "file_id": "BAACAgUAAxkBAAICkWnexVRfFFzJPXAcksEcOHH969k7AAKmGQACEHiBVneBd1h_Jr24OwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه چهارم: لوازم مورد نیاز ترید\n🔘قسمت دوم\n\n✅ در این جلسه یاد می‌گیریم چطور اطلاعات و اخبار بازار را جمع‌آوری و فیلتر کنیم، با سایت‌های مهم اقتصادی و تحلیلی آشنا می‌شویم.\n\n@cafetradetvaf"
    },
    "beg1_3_5a": {
        "title": "جلسه پنجم: مفاهیم پایه ترید و مدیریت ریسک (قسمت اول)",
        "file_id": "BAACAgUAAxkBAAICkmnexVT9YrWx4UnM_eXMNv2qWq-wAAKZIQAC0bSpVkVS06WVPECkOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه پنجم: مفاهیم پایه ترید و مدیریت ریسک\n🔘قسمت اول\n\n✅ در این جلسه با مفاهیم مهم و اصطلاحات پایه ترید آشنا می‌شویم، انواع سفارش‌ها و بازارها را یاد می‌گیریم.\n\n@cafetradetvaf"
    },
    "beg1_3_5b": {
        "title": "جلسه پنجم: مفاهیم پایه ترید و مدیریت سرمایه (قسمت دوم)",
        "file_id": "BAACAgUAAxkBAAICk2nexVSRUt3cijQt7TxczYaN2W7RAAK5IQAC0bSpVkeQNNeFDycPOwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه پنجم: مفاهیم پایه ترید و مدیریت سرمایه\n🔘قسمت دوم\n\n@cafetradetvaf"
    },
    "beg1_3_5c": {
        "title": "جلسه پنجم: مفاهیم پایه ترید و مدیریت سرمایه (قسمت سوم)",
        "file_id": "BAACAgUAAxkBAAIClGnexVRFbTkiO_s2akEfKG1AAdo6AALOIQAC0bSpVkqiON0wEfY9OwQ",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه پنجم: مفاهیم پایه ترید و مدیریت سرمایه\n🔘قسمت سوم\n\n@cafetradetvaf"
    },
    "beg1_3_6": {
        "title": "جلسه ششم: آشنایی با بروکر، صرافی و ولت",
        "file_id": "BAACAgUAAxkBAAICe2new5543VDCtfhooAABkkwg3GvMOwACIh8AArj28VaKB2EMa4_qiTsE",
        "caption": "📚 فصل اول: ابتدایی\n📊 بخش سوم: ابزار کاربردی\n🎓 جلسه ششم: آشنایی با بروکر، صرافی و ولت\n\n✅ در این جلسه با مفهوم کیف پول (Wallet) و انواع آن آشنا می‌شویم، تفاوت بین بروکر و صرافی را یاد می‌گیریم و نکات مهم امنیتی برای حفظ دارایی را بررسی می‌کنیم.\n\n@cafetradetvaf"
    },

    "details_more": {
        "title": "جزییات بیشتر",
        "link": "https://t.me/Amuzesh_cafetradeTvaf/84"
    }
}

menu_structure = {
    "فصل اول: ابتدایی": {
        "بخش اول: بازارهای مالی": ["beg1_1_1", "beg1_1_2", "beg1_1_3", "beg1_1_4", "beg1_1_5", "beg1_1_6"],
        "بخش دوم: تحلیل بازار": ["beg1_2_1", "beg1_2_2", "beg1_2_3", "beg1_2_4", "beg1_2_5", "beg1_2_6"],
        "بخش سوم: ابزار کاربردی": ["beg1_3_1", "beg1_3_2", "beg1_3_3", "beg1_3_4a", "beg1_3_4b", "beg1_3_5a", "beg1_3_5b", "beg1_3_5c", "beg1_3_6"],
    },
    "فصل دوم: پیشرفته": {},
    "فصل سوم: پروژه عملی": {}
}

MAIN_MENU_TEXT = "سیستم آموزشی بازارهای مالی صفر تا صد\nلطفاً انتخاب کنید:"
user_state = {}
user_names = {}

ASK_NAME = 1


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


def main_menu(chat_id):
    items = [
        {"title": "معرفی دوره", "callback": "intro"},
        {"title": "فصل اول: ابتدایی", "callback": "f1"},
        {"title": "فصل دوم: پیشرفته", "callback": "f2"},
        {"title": "فصل سوم: پروژه عملی", "callback": "f3"},
        {"title": "جزییات بیشتر", "link": sessions['details_more']['link']}
    ]
    return MAIN_MENU_TEXT, build_buttons(items, chat_id)


def get_section_back(menu_key):
    if menu_key == "f1":
        return "f1"
    elif menu_key == "f2":
        return "f2"
    elif menu_key == "f3":
        return "f3"
    return "main"


def get_menu(chat_id):
    state = user_state.get(chat_id, {})
    menu = state.get("menu", "main")

    if menu == "main":
        return main_menu(chat_id)

    if menu in ("f1", "f2", "f3"):
        f_map = {"f1": "فصل اول: ابتدایی", "f2": "فصل دوم: پیشرفته", "f3": "فصل سوم: پروژه عملی"}
        f_key = f_map[menu]
        sections = list(menu_structure[f_key].keys())
        if not sections:
            return f"{f_key}\n⚠️ هنوز آماده نیست", InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت", callback_data="main")]])
        items = [{"title": s, "callback": f"sec|{menu}|{i}"} for i, s in enumerate(sections)]
        return f_key, build_buttons(items, chat_id, "main")

    if menu.startswith("sec|"):
        _, f_code, idx = menu.split("|")
        idx = int(idx)
        f_map = {"f1": "فصل اول: ابتدایی", "f2": "فصل دوم: پیشرفته", "f3": "فصل سوم: پروژه عملی"}
        f_key = f_map[f_code]
        sections = list(menu_structure[f_key].keys())
        section_name = sections[idx]
        sess_list = menu_structure[f_key][section_name]
        items = [{"title": sessions[s]["title"], "callback": s} for s in sess_list]
        return section_name, build_buttons(items, chat_id, f_code)

    return main_menu(chat_id)


async def send_menu(context, chat_id):
    name = user_names.get(chat_id, "")
    greeting = f"👋 خوش اومدی {name}!\n\n" if name else ""
    text, markup = get_menu(chat_id)
    full_text = greeting + text
    old_msg_id = user_state.get(chat_id, {}).get("menu_msg_id")
    if old_msg_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except Exception:
            pass
    msg = await context.bot.send_message(chat_id=chat_id, text=full_text, reply_markup=markup)
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["menu_msg_id"] = msg.message_id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_state[chat_id] = {"last_session": None, "menu": "main", "menu_msg_id": None}

    if chat_id in user_names:
        name = user_names[chat_id]
        await update.message.reply_text(
            f"👋 سلام {name}!\nخوش برگشتی به سیستم آموزشی بازارهای مالی."
        )
        await send_menu(context, chat_id)
        return ConversationHandler.END

    await update.message.reply_text(
        "🎓 سلام! به سیستم آموزشی بازارهای مالی صفر تا صد خوش اومدی!\n\n"
        "📝 لطفاً اسمت رو بنویس تا بتونیم بهتر کمکت کنیم:\n\n"
        "💡 دفعه‌های بعد با /شروع وارد بشو"
    )
    return ASK_NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.message.text.strip()

    if not name or len(name) > 50:
        await update.message.reply_text("لطفاً یک اسم معتبر وارد کن:")
        return ASK_NAME

    user_names[chat_id] = name
    if chat_id not in user_state:
        user_state[chat_id] = {"last_session": None, "menu": "main", "menu_msg_id": None}

    await update.message.reply_text(
        f"✅ ممنون {name}! حالا می‌تونی شروع کنی به یادگیری."
    )
    await send_menu(context, chat_id)
    return ConversationHandler.END


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

    if data in ("f1", "f2", "f3"):
        user_state[chat_id]["menu"] = data
        await send_menu(context, chat_id)
        return

    if data.startswith("sec|"):
        user_state[chat_id]["menu"] = data
        await send_menu(context, chat_id)
        return

    if data == "intro":
        user_state[chat_id]["last_session"] = "intro"
        await context.bot.send_video(
            chat_id=chat_id,
            video=sessions["intro"]["file_id"],
            caption=sessions["intro"]["caption"]
        )
        await send_menu(context, chat_id)
        return

    if data == "last":
        last = user_state[chat_id].get("last_session")
        if last and last in sessions and "file_id" in sessions[last]:
            await context.bot.send_video(
                chat_id=chat_id,
                video=sessions[last]["file_id"],
                caption=sessions[last]["caption"]
            )
            await send_menu(context, chat_id)
        return

    if data in sessions and "file_id" in sessions[data]:
        user_state[chat_id]["last_session"] = data
        await context.bot.send_video(
            chat_id=chat_id,
            video=sessions[data]["file_id"],
            caption=sessions[data]["caption"]
        )
        await send_menu(context, chat_id)
        return


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error:", exc_info=context.error)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("شروع", start),
        ],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("شروع", start),
        ],
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    print("Bot Running...")
    app.run_polling()