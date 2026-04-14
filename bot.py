from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8648252290:AAFLlbGXst4s2hhOWK1uRIGtd0Is9Zlkb34"

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        await update.message.reply_text(update.message.video.file_id)
    else:
        await update.message.reply_text("فقط ویدیو بفرست")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, get_id))

print("Running...")
app.run_polling()