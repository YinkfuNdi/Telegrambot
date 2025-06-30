from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# keyboards/main_menu.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu(cart_count=0, orders_count=0):
    keyboard = [
        [InlineKeyboardButton("🤔 How does it work?", callback_data="how_it_works")],
        [
            InlineKeyboardButton("✋ Help", callback_data="help"),
            InlineKeyboardButton("📘 User Guide", callback_data="user_guide")
        ],
        [InlineKeyboardButton("🎁 Products", callback_data="products")],
        [
          InlineKeyboardButton("📝 Reviews", callback_data="reviews"),

            InlineKeyboardButton("📢 Ref & Earn", callback_data="ref_earn")
            
        ],
        [
            InlineKeyboardButton("💳 Coupon", callback_data="coupon"),
            InlineKeyboardButton("❤️ Friendly Services", callback_data="friendly_services")
        ],
        [InlineKeyboardButton("❓ FAQs", callback_data="faqs")],
        [
            InlineKeyboardButton(f"🛒 Cart ({cart_count})", callback_data="view_cart"),
            InlineKeyboardButton(f"📦 Orders ({orders_count})", callback_data="orders")
        ],
        [InlineKeyboardButton("🔙 Back to Countries", callback_data="back_to_countries")]
    ]
    return InlineKeyboardMarkup(keyboard)
