from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from keyboards.main_menu import main_menu
from keyboards.country_selector import country_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 Welcome to our store", reply_markup=main_menu())

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔷 Main Menu\nChoose an option below:", reply_markup=main_menu())

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'how_it_works':
        await query.edit_message_text("🧠 Here's how it works...")
    elif query.data == 'help':
        await query.edit_message_text("👋 How can I help you?")
    elif query.data == 'user_guide':
        await query.edit_message_text("📖 This is your user guide...")

    # ✅ If a country is selected, show its service menu
    elif query.data in ['Cameroon', 'Nigeria']:
        context.user_data["country"] = query.data  # Optional tracking
        keyboard = [
            [InlineKeyboardButton("🌿 Buy Weed", callback_data='buy_weed')],
            [InlineKeyboardButton("🍪 Edibles", callback_data='buy_edibles')],
            [InlineKeyboardButton("💨 Vapes", callback_data='buy_vapes')],
            [InlineKeyboardButton("🔙 Back to Countries", callback_data='select_country')]
        ]
        await query.edit_message_text(
            text=f"🇨🇲 Welcome to {query.data}'s Menu. Choose a service:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ✅ Handle menu item selections
    elif query.data == 'buy_weed':
        await query.edit_message_text("🌿 Available Weed Strains:\n- OG Kush\n- Purple Haze\n- Gelato")
    elif query.data == 'buy_edibles':
        await query.edit_message_text("🍪 Available Edibles:\n- THC Cookies\n- Brownies\n- Gummies")
    elif query.data == 'buy_vapes':
        await query.edit_message_text("💨 Vape Selection:\n- Strawberry Carts\n- Lemon Haze Pen")
    elif query.data == 'select_country':
        await query.edit_message_text("🌍 Choose your country:", reply_markup=country_menu())
