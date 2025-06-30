from telegram import Update
from telegram.ext import ContextTypes

async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📞 Support: @The1010Boys_Support\n📸 Instagram: @The1010Boys.EU")
