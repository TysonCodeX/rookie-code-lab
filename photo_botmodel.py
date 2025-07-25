# 📦 Telegram Photo & File Storage Bot (Upgraded)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os

# 🔐 Telegram Bot Token
TOKEN = "1234567891013345789986433"  # 🔁 Replace with your real bot token

# 📂 Directory to save files/photos
SAVE_DIR = "/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/"

# Ensure the save directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 📥 Save incoming photo
async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    sender = update.message.from_user.username or "user"
    short_id = file.file_id[-10:]  # ✅ Make short to avoid "invalid callback data"
    filename = f"{sender}_{short_id}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)

    await file.download_to_drive(filepath)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬇️ Open", url=file.file_path)],
        [InlineKeyboardButton("🗑️ Delete", callback_data=f"del|{filename}")]
    ])

    await update.message.reply_text("✅ Photo saved!", reply_markup=keyboard)

# 📁 Save incoming files (documents, etc.)
async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    file = await context.bot.get_file(doc.file_id)

    sender = update.message.from_user.username or "user"
    short_id = doc.file_id[-10:]
    filename = f"{sender}_{short_id}_{doc.file_name}"
    filepath = os.path.join(SAVE_DIR, filename)

    await file.download_to_drive(filepath)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬇️ Open", url=file.file_path)],
        [InlineKeyboardButton("🗑️ Delete", callback_data=f"del|{filename}")]
    ])

    await update.message.reply_text("✅ File saved!", reply_markup=keyboard)

# 🗑️ Delete handler
async def handle_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    try:
        await query.answer()
    except:
        pass  # Avoid crash if user clicked too late

    if not query.data.startswith("del|"):
        await query.edit_message_text("⚠️ Invalid button.")
        return

    filename = query.data.split("|")[1]
    filepath = os.path.join(SAVE_DIR, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        await query.edit_message_text("🗑️ Deleted successfully.")
    else:
        await query.edit_message_text("⚠️ File not found.")

# 🚀 Start bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, save_photo))
app.add_handler(MessageHandler(filters.Document.ALL, save_file))
app.add_handler(CallbackQueryHandler(handle_delete, pattern=r"^del\|"))

print("🤖 Bot is running and ready!")
app.run_polling()
