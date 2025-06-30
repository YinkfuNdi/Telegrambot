import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(level=logging.INFO)

COUNTRIES = ["Austria", "Germany", "France"]
PRODUCTS = ["Blue Dream", "OG Kush", "White Widow"]

ASK_NAME, ASK_ADDRESS, ASK_PAYMENT = range(3)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("Products", callback_data="products")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_country_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(c, callback_data=f"country_{c}")] for c in COUNTRIES]
    )

def get_products_keyboard():
    keyboard = [[InlineKeyboardButton(f"Add {p}", callback_data=f"add_{p}")] for p in PRODUCTS]
    keyboard.append([
        InlineKeyboardButton("🛒 View Cart", callback_data="view_cart"),
        InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_menu")
    ])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Please select your country:", reply_markup=get_country_keyboard()
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("country_"):
        country = data[len("country_"):]
        context.user_data['country'] = country
        await query.edit_message_text(
            f"Country set to *{country}*.\n\nChoose from menu:", parse_mode="Markdown",
            reply_markup=main_menu()
        )
    elif data == "products":
        await query.edit_message_text("Choose products to add:", reply_markup=get_products_keyboard())
    elif data.startswith("add_"):
        product = data[len("add_"):]
        cart = context.user_data.get("cart", [])
        cart.append(product)
        context.user_data["cart"] = cart
        # Just answer callback to notify user, don't edit message here
        await query.answer(f"Added {product} to cart.")
    elif data == "view_cart":
        cart = context.user_data.get("cart", [])
        if not cart:
            await query.edit_message_text("Your cart is empty.", reply_markup=get_products_keyboard())
        else:
            text = "🛒 Your cart:\n" + "\n".join(f"• {item}" for item in cart)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Checkout", callback_data="checkout")],
                [InlineKeyboardButton("Clear Cart", callback_data="clear_cart")],
                [InlineKeyboardButton("Back to Products", callback_data="products")]
            ])
            await query.edit_message_text(text, reply_markup=keyboard)
    elif data == "clear_cart":
        context.user_data["cart"] = []
        await query.edit_message_text("Cart cleared.", reply_markup=get_products_keyboard())
    elif data == "back_to_menu":
        await query.edit_message_text("Main menu:", reply_markup=main_menu())
    elif data == "help":
        await query.edit_message_text("This is a simple bot demo. Use the menu to shop.")
    else:
        await query.edit_message_text(f"Unknown command: {data}")

async def start_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cart = context.user_data.get("cart", [])
    if not cart:
        await query.edit_message_text("Your cart is empty, add products before checkout.")
        return ConversationHandler.END
    else:
        await query.edit_message_text("Please enter your full name:")
        return ASK_NAME

async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Now enter your delivery address:")
    return ASK_ADDRESS

async def ask_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("BTC", callback_data="pay_btc")],
        [InlineKeyboardButton("USDT", callback_data="pay_usdt")],
        [InlineKeyboardButton("Cancel", callback_data="cancel_checkout")]
    ])
    await update.message.reply_text("Choose payment method:", reply_markup=keyboard)
    return ASK_PAYMENT

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cancel_checkout":
        await query.edit_message_text("Checkout cancelled.")
        return ConversationHandler.END

    payment = "BTC" if query.data == "pay_btc" else "USDT"
    context.user_data["payment"] = payment
    name = context.user_data.get("name")
    address = context.user_data.get("address")
    cart = context.user_data.get("cart", [])

    order_summary = "\n".join(f"• {item}" for item in cart)
    await query.edit_message_text(
        f"Order confirmed!\n\nName: {name}\nAddress: {address}\nPayment: {payment}\n\nItems:\n{order_summary}"
    )
    context.user_data["cart"] = []
    return ConversationHandler.END

async def cancel_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Checkout cancelled.")
    return ConversationHandler.END

def main():
    import os
    TOKEN = os.getenv("8067569796:AAEG4iwuNHQWfzTy9zO11LbNU9OnDrMVzLI")  # Make sure to set this env var, or replace with the string token directly
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    ...


    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_checkout, pattern="^checkout$")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), ask_address)],
            ASK_ADDRESS: [MessageHandler(filters.TEXT & (~filters.COMMAND), ask_payment)],
            ASK_PAYMENT: [CallbackQueryHandler(confirm_order, pattern="^(pay_btc|pay_usdt|cancel_checkout)$")]
        },
        fallbacks=[CommandHandler("cancel", cancel_checkout)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
