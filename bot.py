import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"  # توکن ره مستقیم اینجا بگذار

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"📌 FILE ID:\n{file_id}")
    else:
        await update.message.reply_text("❌ فقط ویدیو بفرست")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, get_file_id))

    print("Bot Running...")
    app.run_polling()