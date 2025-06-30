from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters, ContextTypes
)
import logging

import json

with open("reviews.json", "r") as file:
    REVIEWS = json.load(file)


# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants ---
COUNTRIES = [
    "Austria", "Germany", "France", "Switzerland", "Spain",
    "United Kingdom", "Italy", "Netherlands", "Portugal",
]

CATEGORIES = {
    "the_1010_boys": {
        "name": "The 10/10 Boys",
        "subcategories": {
            "the_1010_boys_1g": {
                "name": "The 10/10 boys - 1g",
                "products": {
                    "mint_chocolate_chip": {
                        "name": "Mint Chocolate Chip - 1g",
                        "price": "520€/unit",
                        "description": "Potent hybrid with a smooth minty finish.",
                        "quantities": ["1g"]
                    },
                    "wizard_tree": {
                        "name": "Wizard Tree - Sativa - 1g",
                        "price": "50€/unit",
                        "description": "Wizard Tree is a premium Sativa strain known for its vibrant, crystal-coated buds and an invigorating citrus-pine aroma. It delivers an energetic, creative high perfect for daytime use, focus, and socializing—ideal for those seeking motivation and mental clarity without the heaviness.",
                        "quantities": ["1g"]
                    },
                    "golden_pineapple": {
                        "name": "Golden Pineapple - Sativa - 1g",
                        "price": "50€/unit",
                        "description": "Tropical sativa with sweet aroma.",
                        "quantities": ["1g"]
                    },
                    "snoop_dogg_og": {
                        "name": "Snoop Dogg OG - Indica - 1g",
                        "price": "50€/unit",
                        "description": "Relaxing indica for evening use.",
                        "quantities": ["1g"]
                    },
                    "watermelon_gelato": {
                        "name": "Watermelon Gelato - Indica - 1g",
                        "price": "50€/unit",
                        "description": "Fruity indica strain, smooth taste.",
                        "quantities": ["1g"]
                    }
                }
            },
            "the_1010_boys_2g": {
                "name": "The 10/10 boys - 2g",
                "price": "60€/unit",
                "description": "Premium quality 2g pack of the 10/10 boys strain.",
                "quantities": ["2g"]
            }
        }
    }
}

def main_menu(user_id=0, bot_data={}):
    cart_count = len(bot_data.get("cart", {}).get(user_id, []))
    orders_count = len(bot_data.get("orders", {}).get(user_id, []))
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤔 How does it work?", callback_data="how_it_works")],
        [InlineKeyboardButton("✋ Help", callback_data="help"),
         InlineKeyboardButton("📘 User Guide", callback_data="user_guide")],
        [InlineKeyboardButton("🎁 Products", callback_data="products")],
        [InlineKeyboardButton("📊 Reviews", callback_data="reviews"),
         InlineKeyboardButton("📢 Ref & Earn", callback_data="ref_earn")],
        [InlineKeyboardButton("🏷 Coupon", callback_data="coupon"),
         InlineKeyboardButton("❤️ Friendly Services", callback_data="friendly_services")],
        [InlineKeyboardButton("❓ FAQs", callback_data="faqs")],
        [InlineKeyboardButton(f"🛒 Cart ({cart_count})", callback_data="cart"),
         InlineKeyboardButton(f"📦 Orders ({orders_count})", callback_data="orders")]
    ])



# Conversation states
COLLECT_NAME, COLLECT_PHONE, COLLECT_ADDRESS, CONFIRM_ORDER, PAYMENT_PROCESS = range(5)

# In-memory storage (for simplicity)
user_carts = {}
user_order_details = {}

# --- UI Keyboards ---
def keyboard_from_list(options, prefix):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(opt, callback_data=f"{prefix}_{opt.replace(' ', '_')}")] for opt in options
    ])
    

def main_menu_keyboard():
    buttons = [
        ("🏡 Main Menu", "main_menu"),
        ("🌟 View Cart", "view_cart"),
        ("💳 Checkout", "checkout")
    ]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=data)] for text, data in buttons
    ])

def categories_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(data["name"], callback_data=f"category_{key}")]
         for key, data in CATEGORIES.items()
    ])

def subcategories_keyboard(category_key):
    category = CATEGORIES.get(category_key)
    if not category:
        return InlineKeyboardMarkup([])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(sub["name"], callback_data=f"subcategory|{category_key}|{sub_key}")]
         for sub_key, sub in category["subcategories"].items()
    ])

def quantity_keyboard(category_key, subcategory_key):
    quantities = CATEGORIES[category_key]["subcategories"][subcategory_key].get("quantities", [])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(q, callback_data=f"quantity_{category_key}_{subcategory_key}_{q}")] for q in quantities
    ])


def cart_keyboard(user_id):
    cart = user_carts.get(user_id, [])
    if not cart:
        return InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Cart is empty", callback_data="empty")]])
    keyboard = [
        [InlineKeyboardButton(f"Remove: {item['product_name']} ({item['quantity']})", callback_data=f"remove_{i}")]
        for i, item in enumerate(cart)
    ]
    keyboard.append([InlineKeyboardButton("✅ Checkout", callback_data="checkout")])
    keyboard.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_carts[user_id] = []  # Reset cart on /start
    await update.message.reply_text(
        "Welcome! Select your country:",
        reply_markup=keyboard_from_list(COUNTRIES, "country")
    )

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    if data.startswith("country_"):
        # User selected country, show categories
        await query.edit_message_text("Select a category:", reply_markup=categories_keyboard())
        return

    elif data.startswith("category_"):
        # User selected a category, show subcategories
        category_key = data.split("_", 1)[1]
        await query.edit_message_text("Choose a product:", reply_markup=subcategories_keyboard(category_key))
        return

    elif data.startswith("subcategory|"):
        # User selected a subcategory, show product details + quantity keyboard
        parts = data.split("|")
        if len(parts) != 3:
            await query.edit_message_text("⚠️ Invalid subcategory selection.")
            return
        _, cat_key, sub_key = parts
        category = CATEGORIES.get(cat_key)
        
    if data == "reviews":
        await query.edit_message_text(get_all_reviews(), parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))


        
        if not category:
            await query.edit_message_text("⚠️ Unknown category.")
            return
        product = category["subcategories"].get(sub_key)
        if not product:
            await query.edit_message_text("⚠️ Unknown product.")
            return

        caption = f"📦 {product['name']}\n\n"
        if "price" in product:
            caption += f"Price: {product['price']}\n\n"
        caption += product.get("description", "No description available.")

        await query.edit_message_media(
            media=InputMediaPhoto(media=product["image_url"], caption=caption),
            reply_markup=quantity_keyboard(cat_key, sub_key)
        )
        return

    elif data.startswith("add__"):
        # Add product with quantity to cart
        parts = data.split("__")
        if len(parts) != 4:
            await query.edit_message_text("⚠️ Invalid add to cart command.")
            return
        _, cat_key, sub_key, qty = parts
        category = CATEGORIES.get(cat_key)
        if not category:
            await query.edit_message_text("⚠️ Unknown category.")
            return
        product = category["subcategories"].get(sub_key)
        if not product:
            await query.edit_message_text("⚠️ Product not found.")
            return
        # Add to user's cart
        user_carts.setdefault(user_id, []).append({
            "product_name": product["name"],
            "quantity": qty,
            "price": product.get("price", "N/A")
        })
        await query.edit_message_caption(
            caption=f"✅ Added to cart: {product['name']} ({qty})",
            reply_markup=main_menu_keyboard()
        )
        return

    elif data == "view_cart":
        cart = user_carts.get(user_id, [])
        if not cart:
            await query.edit_message_text("🛒 Your cart is empty.", reply_markup=main_menu_keyboard())
        else:
            cart_text = "\n".join(
                [f"{item['product_name']} ({item['quantity']}) - {item['price']}" for item in cart]
            )
            await query.edit_message_text(f"Your cart:\n\n{cart_text}", reply_markup=cart_keyboard(user_id))
        return

    elif data.startswith("remove_"):
        index_str = data.split("_", 1)[1]
        try:
            index = int(index_str)
        except ValueError:
            await query.edit_message_text("⚠️ Invalid remove command.", reply_markup=main_menu_keyboard())
            return
        cart = user_carts.get(user_id, [])
        if 0 <= index < len(cart):
            removed = cart.pop(index)
            await query.edit_message_text(f"Removed: {removed['product_name']}", reply_markup=cart_keyboard(user_id))
        else:
            await query.edit_message_text("⚠️ Item not found in cart.", reply_markup=main_menu_keyboard())
        return

    elif data == "main_menu":
        # Show country selection again (you can modify if needed)
        await query.edit_message_text("Welcome back! Select your country:", reply_markup=keyboard_from_list(COUNTRIES, "country"))
        return

    elif data == "checkout":
        cart = user_carts.get(user_id, [])
        if not cart:
            await query.answer("Your cart is empty!", show_alert=True)
            return ConversationHandler.END
        await query.message.edit_text("👤 What's your full name?")
        return COLLECT_NAME

    else:
        await query.edit_message_text("⚠️ Unknown option selected.", reply_markup=main_menu_keyboard())

# --- Checkout Conversation Handlers ---
async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_order_details[user_id] = {"name": update.message.text}
    await update.message.reply_text("📱 Enter your phone number:")
    return COLLECT_PHONE

async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_order_details[user_id]["phone"] = update.message.text
    await update.message.reply_text("🏠 Enter your delivery address:")
    return COLLECT_ADDRESS

async def collect_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_order_details[user_id]["address"] = update.message.text
    details = user_order_details[user_id]

    cart = user_carts.get(user_id, [])
    cart_summary = "\n".join([f"{item['product_name']} ({item['quantity']}) - {item['price']}" for item in cart])

    await update.message.reply_text(
        f"Please confirm your order:\n\n"
        f"Name: {details['name']}\n"
        f"Phone: {details['phone']}\n"
        f"Address: {details['address']}\n\n"
        f"Order items:\n{cart_summary}\n\nConfirm? (yes/no)"
    )
    return CONFIRM_ORDER

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.text.strip().lower() == "yes":
        await update.message.reply_text(
            "✅ Order confirmed! Proceed to payment (simulated).\n"
            "Type 'done' when you have completed the payment."
        )
        return PAYMENT_PROCESS
    else:
        await update.message.reply_text("Order canceled.", reply_markup=main_menu_keyboard())
        user_order_details.pop(user_id, None)
        return ConversationHandler.END

async def simulate_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.text.strip().lower() == "done":
        await update.message.reply_text(
            "💸 Payment confirmed. Your order will be shipped soon!",
            reply_markup=main_menu_keyboard()
        )
        # Clear data for next order
        user_carts.pop(user_id, None)
        user_order_details.pop(user_id, None)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please type 'done' when payment is completed.")
        return PAYMENT_PROCESS

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Order process canceled.", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

# --- Main Application Setup ---
def main():
    TOKEN = "8067569796:AAEG4iwuNHQWfzTy9zO11LbNU9OnDrMVzLI"  # Replace with your bot token

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(callback_router, pattern="^checkout$")],
        states={
            COLLECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_name)],
            COLLECT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_phone)],
            COLLECT_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_address)],
            CONFIRM_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)],
            PAYMENT_PROCESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, simulate_payment)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    


    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(callback_router))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()

def get_all_reviews():
    text = "📊 *User Reviews:*\n\n"
    for product_key, review_list in REVIEWS.items():
        product_name = CATEGORIES["the_1010_boys"]["subcategories"]["the_1010_boys_1g"]["products"].get(product_key, {}).get("name", product_key.replace("_", " ").title())
        text += f"📦 *{product_name}*:\n"
        for r in review_list:
            text += f"{r}\n"
        text += "\n"
    return text
