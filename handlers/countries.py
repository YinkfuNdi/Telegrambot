from telegram import Update
from telegram.ext import ContextTypes

async def country_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data.replace("country_", "").capitalize()
    await query.edit_message_text(f"🌍 You selected: {country}")
