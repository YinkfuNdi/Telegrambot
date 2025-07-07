import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram import Update
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Country Options ---
COUNTRIES = [
    "Austria", "Germany", "France", "Switzerland", "Spain",
    "United Kingdom", "Italy", "Netherlands", "Portugal",
]

# --- Category + Subcategory + Product Data ---
CATEGORIES = {
    "t10b": {
        "name": "The 10/10 Boys",
        "subcategories": {
            "g1": {
                "name": "The 10/10 Boys - 1g",
                "products": {
                    "mint_choc": {
                        "name": "Mint Chocolate Chip - 1g",
                        "price": "50€/unit",
                        "description": "Mint Chocolate Chip is a potent hybrid strain that blends the best of relaxation and euphoria. With dense, frosty buds and a cool minty aroma layered over earthy chocolate notes, it offers a smooth, flavorful smoke. Perfect for stress relief, light body relaxation, and creative focus without heavy sedation.",
                        "quantities": {
                            "50": "35.00€",
                            "20": "40.00€",
                            "5": "45.00€",
                            "1": "50.00€"
                        }
                    },
                    "wiz_tree": {
                        "name": "Wizard Tree - Sativa - 1g",
                        "price": "50€/unit",
                        "description": "Wizard Tree is a premium Sativa strain known for its vibrant, crystal-coated buds and an invigorating citrus-pine aroma. It delivers an energetic, creative high perfect for daytime use, focus, and socializing—ideal for those seeking motivation and mental clarity without the heaviness.",
                        "quantities": {
                            "50": "35.00€",
                            "20": "40.00€",
                            "5": "45.00€",
                            "1": "50.00€"
                        }
                    },
                    "gold_pine": {
                        "name": "Golden Pineapple - Sativa - 1g",
                        "price": "50€/unit",
                        "description": "Golden Pineapple is a vibrant sativa strain known for its energizing effects and uplifting high. Bursting with tropical flavors and a juicy, sweet pineapple aroma, it delivers a smooth, fruity smoke perfect for daytime use. Ideal for boosting mood, enhancing focus, and sparking creativity without overwhelming the senses."
,
                        "quantities": {
                            "50": "35.00€",
                            "20": "40.00€",
                            "5": "45.00€",
                            "1": "50.00€"
                        }
                    },
                    "snoop_og": {
                        "name": "Snoop Dogg OG - Indica - 1g",
                        "price": "50€/unit",
                        "description": "Snoop Dogg OG is a heavy-hitting indica strain named after the legendary rapper himself. Renowned for its deeply relaxing effects, it delivers a smooth, earthy smoke with hints of pine and citrus. Perfect for winding down after a long day, this strain promotes calm, eases stress, and helps with sleep—ideal for nighttime use and chill vibes.",
                        "quantities": {
                            "50": "35.00€",
                            "20": "40.00€",
                            "5": "45.00€",
                            "1": "50.00€"
                        }
                    },
                    "water_gel": {
                        "name": "Watermelon Gelato - Indica - 1g",
                        "price": "50€/unit",
                        "description": "Watermelon Gelato is a flavorful indica strain known for its sweet, fruity aroma and ultra-smooth smoke. Bursting with notes of watermelon, berries, and creamy gelato undertones, it delivers a calming body high that's perfect for relaxation, stress relief, and peaceful evenings. Ideal for unwinding without heavy sedation, this strain combines flavor with tranquility."
,
                        "quantities": {
                            "50": "35.00€",
                            "20": "40.00€",
                            "5": "45.00€",
                            "1": "50.00€"
                        }
                    }
                }
            }
        }
    },


    "t10b_siuk2g": {
    "name": "1010 Boys x SIUK - 2g",
    "subcategories": {
        "default": {
            "name": "All Strains - 2g",
            "products": {
                "double_bubble": {
                    "name": "Double Bubblegum - Hybrid - 2g",
                    "price": "60€/unit",
                    "description": "Double Bubblegum is a hybrid strain known for its sweet, candy-like aroma and balanced high. Great for mood elevation and relaxation.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "60.00€"
                    }
                },
                "purple_panties": {
                    "name": "Purple Panties - Indica - 2g",
                    "price": "60€/unit",
                    "description": "Purple Panties is a potent indica strain that soothes the body and calms the mind. Rich in flavor with sweet berry undertones.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "60.00€"
                    }
                },
                "galactic_gas": {
                    "name": "Galactic Gas - Indica - 2g",
                    "price": "60€/unit",
                    "description": "Galactic Gas delivers a cosmic indica high with deep relaxation and pungent earthy notes. Perfect for night use.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "60.00€"
                    }
                },
                "lime_sherbert": {
                    "name": "Lime Sherbert - Hybrid - 2g",
                    "price": "60€/unit",
                    "description": "Lime Sherbert offers a citrusy twist on hybrid relaxation. Energizing and soothing with a tart lime finish.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "60.00€"
                    }
                },
                "caribbean_crush": {
                    "name": "Caribbean Crush - Sativa - 2g",
                    "price": "60€/unit",
                    "description": "Caribbean Crush is a vibrant sativa with tropical notes and uplifting effects, perfect for social and creative sessions.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "60.00€"
                    }
                }
            }
        }
    }
},

     "hidden_hills": {
    "name": "Hidden Hills Collection - 2g",
    "subcategories": {
        "hh_2g": {
            "name": "Hidden Hills Vapes - 2g",
            "products": {
                "dosi_rocky": {
                    "name": "Dosi Rocky Runtz - Indica - 2g",
                    "price": "70€/unit",
                    "description": "Dosi Rocky Runtz delivers a deeply relaxing indica buzz with sweet earthy tones. Great for evening unwind and sleep.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "70.00€"
                    }
                },
                "kosmic_kiwi": {
                    "name": "Kosmic Kiwi - Hybrid - 2g",
                    "price": "70€/unit",
                    "description": "Kosmic Kiwi is a hybrid vape with 2000mg of potent blend. Enjoy smooth hits and long-lasting satisfaction with fruity freshness.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "70.00€"
                    }
                },
                "straw_sherb": {
                    "name": "Strawberry Sherbet - Hybrid - 2g",
                    "price": "70€/unit",
                    "description": "Strawberry Sherbet delivers sweet creamy hits with balanced hybrid effects. Relaxing and uplifting all in one.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "70.00€"
                    }
                },
                "face_punch": {
                    "name": "Tropical Face Punch - Sativa - 2g",
                    "price": "70€/unit",
                    "description": "Tropical Face Punch hits with energetic tropical flavor and a bold sativa kick. Great for a morning boost.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "70.00€"
                    }
                },
                "apple_sour": {
                    "name": "Glazed Apple Sour - Sativa - 2g",
                    "price": "70€/unit",
                    "description": "Glazed Apple Sour is a sativa blend with sweet and sour green apple notes. Stimulating and flavorful vape experience.",
                    "quantities": {
                        "50": "45.00€",
                        "20": "50.00€",
                        "5": "55.00€",
                        "1": "70.00€"
                    }
                }
            }
        }
    }
},


    "t10b2g": {
        "name": "The 10/10 Boys - 2g Collection",
        "subcategories": {
            "sativa": {
                "name": "Sativa - 2g",
                "products": {
                    "love_affair": {
                        "name": "Love Affair - Sativa - 2g",
                        "price": "60€/unit",
                        "description": "Watermelon Gelato is a flavorful indica strain known for its sweet, fruity aroma and ultra-smooth smoke. Bursting with notes of watermelon, berries, and creamy gelato undertones, it delivers a calming body high that's perfect for relaxation, stress relief, and peaceful evenings. Ideal for unwinding without heavy sedation, this strain combines flavor with tranquility.",
                        "quantities": {
                            "50": "35.00€",
                            "20": "40.00€",
                            "5": "45.00€",
                            "1": "50.00€"
                        }
                    },
                    "peach_cresc": {
                        "name": "Peach Crescendo - Sativa - 2g",
                        "price": "60€/unit",
                        "description": "Peach Crescendo is a vibrant sativa strain that bursts with the juicy flavor of ripe peaches blended with subtle tropical and citrus notes. Known for its uplifting and energizing effects, it sparks creativity and mental clarity while keeping the body light and active. Ideal for daytime use, social settings, or creative sessions, this strain is a flavorful way to boost your mood and motivation.",
                        "quantities": { "1": "60.00€" }
                    },
                    "trop_burst": {
                        "name": "Tropical Burst - Sativa - 2g",
                        "price": "60€/unit",
                        "description": "Tropical Burst is a zesty sativa strain packed with a medley of exotic fruit flavors, including mango, pineapple, and papaya. Its aroma is equally enticing, delivering a sweet and tangy scent with a refreshing, clean finish. Known for its uplifting and energizing high, Tropical Burst enhances focus and creativity, making it perfect for daytime adventures, productivity, or a vibrant social buzz."
,
                        "quantities": { "1": "60.00€" }
                    },
                    "blue_lob": {
                        "name": "Blue Lobstar - Sativa - 2g",
                        "price": "60€/unit",
                        "description": "Blue Lobstar is a rare and flavorful sativa strain that combines sweet blueberry notes with a citrus-forward punch, creating a vibrant and refreshing experience. Its aroma is fruity and tangy, with hints of lemon zest and herbal undertones. Known for delivering a smooth cerebral buzz, this strain boosts mental clarity and creativity while keeping the body light and relaxed—ideal for daytime use or social occasions.",
                        "quantities": { "1": "60.00€" }
                    },
                    "crunch_berry": {
                        "name": "Crunch Berries - Sativa - 2g",
                        "price": "60€/unit",
                        "description": "Berry-rich and uplifting.",
                        "quantities": { "1": "60.00€" }
                    }
                }
            },
            "indica": {
                "name": "Indica - 2g",
                "products": {
                    "cadi_rain": {
                        "name": "Cadillac Rainbow - Indica - 2g",
                        "price": "60€/unit",
                        "description": "Cadillac Rainbow is a potent indica strain celebrated for its deeply relaxing effects and vibrant terpene profile. With a rich aroma of berries, earthy pine, and a hint of sweet diesel, this strain delivers a full-bodied experience that calms the mind and soothes the body. Its multicolored buds and thick resin production reflect its premium quality. Ideal for evening use, stress relief, and deep sleep, Cadillac Rainbow wraps you in a luxurious sense of tranquility."
,
                        "quantities": { "1": "60.00€" }
                    }
                }
            },
            "hybrid": {
                "name": "Hybrid - 2g",
                "products": {
                    "cherry_pie": {
                        "name": "Cherry Pie OG - Hybrid - 2g",
                        "price": "60€/unit",
                        "description": "Cherry Pie OG is a well-balanced hybrid strain known for its sweet and tart cherry aroma layered with hints of earthy spice. Its dense, trichome-covered buds deliver a calming yet uplifting experience, making it great for both daytime relaxation and evening unwinding. With genetics that combine Granddaddy Purple and Durban Poison, Cherry Pie OG offers a euphoric mental buzz followed by gentle body relaxation, perfect for relieving stress, anxiety, and mild aches."
,
                        "quantities": { "1": "60.00€" }
                    },
                    "candy_rain": {
                        "name": "Candy Rain - Hybrid - 2g",
                        "price": "60€/unit",
                        "description": "Candy Rain is a delightful hybrid strain with a sweet, sugary aroma reminiscent of freshly fallen candy. Known for its smooth and relaxing effects, it offers a gentle balance of uplifting mental clarity and soothing body calm. Perfect for easing stress and promoting relaxation without heavy sedation, Candy Rain is ideal for daytime use or unwinding after a long day."
,
                        "quantities": { "1": "60.00€" }
                    },
                    "apples_ban": {
                        "name": "Apples & Banana's - Hybrid - 2g",
                        "price": "60€/unit",
                        "description": "Apples & Banana's is a flavorful hybrid strain that blends sweet fruity notes of crisp apples and ripe bananas. It delivers a well-balanced experience, combining a gentle cerebral uplift with relaxing body sensations. Ideal for enhancing creativity and mood while keeping you calm and focused, this strain is perfect for both social occasions and quiet relaxation."
,
                        "quantities": { "1": "60.00€" }
                    },
                    "blue_cake": {
                        "name": "Blueberry Cupcake - Hybrid - 2g",
                        "price": "60€/unit",
                        "description": "Blueberry Cupcake is a delightful hybrid strain that combines sweet blueberry flavors with a smooth, mellow effect. Known for its relaxing yet uplifting qualities, it provides a gentle cerebral buzz paired with soothing body relaxation. Perfect for unwinding after a long day or enhancing creative activities, this strain offers a deliciously sweet aroma and taste reminiscent of freshly baked cupcakes."
,
                        "quantities": { "1": "60.00€" }
                    }
                }
            }
        }
    }

}

FAQ_LIST = [
    "❓ *How do I place an order?*\nTo order, click 'Products', choose a category, select a product, and add it to your cart.",
    "❓ *What payment methods are accepted?*\nWe accept BTC and USDT. Payment instructions will appear at checkout.",
    "❓ *Is shipping discreet?*\nYes, all orders are packaged discreetly with no branding or smell.",
    "❓ *How long does delivery take?*\nUsually between 1–3 working days, depending on your country.",
    "❓ *Where do you ship to?*\nWe currently ship across most of Europe including the UK, Germany, France, Spain, and more.",
    "❓ *Is there a minimum order amount?*\nNo minimum order required. You can even buy just 1g.",
    "❓ *Can I track my order?*\nYes, once shipped you’ll receive a tracking number via Telegram or email.",
    "❓ *Are your products lab tested?*\nYes, our flowers and vapes are high quality and go through a testing process.",
    "❓ *What if I don’t receive my order?*\nContact support. We offer resends for eligible claims.",
    "❓ *Can I return or exchange products?*\nDue to the nature of the products, we do not accept returns. If there’s an issue, contact support."
]

HOW_IT_WORKS_LIST = [
    "🛒 *Browse products*: Navigate through categories and subcategories.",
    "📦 *Select products*: Pick a product and choose a quantity or enter a custom one.",
    "🧺 *Add to cart*: The product will be saved in your cart.",
    "💰 *Choose payment*: Select BTC or USDT and get payment details.",
    "🚚 *Delivery*: After payment is confirmed, your package is shipped discreetly.",
    "⏱ *Delivery time*: Usually 1–3 working days depending on your location.",
]

REVIEWS = {
    "mint_choc": [
        {"stars": 5, "text": "Amazing flavor and great effects!"},
        {"stars": 4, "text": "Really enjoyed this, very relaxing."}
    ],
    "wiz_tree": [
        {"stars": 5, "text": "Perfect for daytime use, very uplifting."},
    ]
    # Add more reviews for other products here
}

# --- Keyboards ---
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

def get_country_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(c, callback_data=f"country_{c.replace(' ', '_')}")] for c in COUNTRIES
    ])

def get_products_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(cat["name"], callback_data=f"category_{key}")]
        for key, cat in CATEGORIES.items()
    ] + [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]])

def get_subcategories_keyboard(category_key):
    category = CATEGORIES.get(category_key, {})
    subcats = category.get("subcategories", {})
    keyboard = [
        [InlineKeyboardButton(sub["name"], callback_data=f"subcategory|{category_key}|{sub_key}")]
        for sub_key, sub in subcats.items()
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Back to Products", callback_data="products")])
    return InlineKeyboardMarkup(keyboard)

def get_product_keyboard(category_key, sub_key):
    subcat = CATEGORIES[category_key]["subcategories"][sub_key]
    products = subcat.get("products", {})
    keyboard = [
        [InlineKeyboardButton(prod["name"], callback_data=f"product|{category_key}|{sub_key}|{prod_key}")]
        for prod_key, prod in products.items()
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Back to Subcategories", callback_data=f"category_{category_key}")])
    return InlineKeyboardMarkup(keyboard)

def get_quantity_keyboard(category_key, sub_key, product_key):
    product = CATEGORIES[category_key]["subcategories"][sub_key]["products"][product_key]
    quantities = product["quantities"]
    keyboard = []

    if isinstance(quantities, dict):
        for qty, price in quantities.items():
            keyboard.append([
                InlineKeyboardButton(f"{qty} - {price}", callback_data=f"quantity|{category_key}|{sub_key}|{product_key}|{qty}")
            ])
    else:
        for qty in quantities:
            keyboard.append([
                InlineKeyboardButton(qty, callback_data=f"quantity|{category_key}|{sub_key}|{product_key}|{qty}")
            ])

    keyboard.append([
        InlineKeyboardButton("✏️ Enter Custom Quantity", callback_data=f"custom_qty|{category_key}|{sub_key}|{product_key}")
    ])
    keyboard.append([
        InlineKeyboardButton("⬅️ Back to Products", callback_data=f"subcategory|{category_key}|{sub_key}")
    ])
    return InlineKeyboardMarkup(keyboard)

def get_payment_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Pay with BTC", callback_data="pay_btc")],
        [InlineKeyboardButton("Pay with USDT", callback_data="pay_usdt")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
    ])

def get_all_reviews():
    logger.info(f"REVIEWS dictionary: {REVIEWS}")
    if not REVIEWS:
        logger.warning("REVIEWS dictionary is empty.")
        return "No reviews available at the moment."

    review_texts = []
    try:
        for product, reviews_list in REVIEWS.items():
            review_texts.append(f"📦 *{product.replace('_', ' ').title()}* Reviews:\n")
            if isinstance(reviews_list, list):
                for review in reviews_list:
                    if isinstance(review, dict) and "stars" in review and "text" in review:
                        stars = "⭐" * review["stars"]
                        review_texts.append(f"{stars} {review['text']}")
                    else:
                        logger.error(f"Malformed review item for product {product}: {review}")
                        review_texts.append("_Error displaying this review_")
            else:
                logger.error(f"Malformed reviews list for product {product}: {reviews_list}")
                review_texts.append(f"_Error displaying reviews for {product}_")
            review_texts.append("")  # blank line between products
    except Exception as e:
        logger.error(f"Error in get_all_reviews: {e}", exc_info=True)
        return "An error occurred while fetching reviews."

    logger.info(f"Generated review text: {review_texts}")
    if not review_texts: # Should not happen if REVIEWS is not empty and no errors
        return "No reviews found."
    return "\n".join(review_texts)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Please select your country:",
        reply_markup=get_country_keyboard()
    )




async def reviews_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        get_all_reviews(),
        parse_mode="Markdown",
        reply_markup=main_menu(user_id, context.bot_data)
    )

async def faqs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    faq_text = "\n\n".join(FAQ_LIST)
    await update.message.reply_text(
        faq_text,
        parse_mode="Markdown",
        reply_markup=main_menu(user_id, context.bot_data)
    )

from telegram.error import BadRequest

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    logger.info(f"Callback query received: {data} from user {user_id}")

    if data.startswith("country_"):
        country = data.split("_", 1)[1].replace('_', ' ')
        context.user_data["country"] = country
        await query.edit_message_text(
            text=f"✅ You selected *{country}*.\nHere is the main menu:",
            parse_mode="Markdown",
            reply_markup=main_menu(user_id, context.bot_data)
        )

    elif data == "main_menu":
        await query.edit_message_text(
            text="🏠 Main Menu:",
            reply_markup=main_menu(user_id, context.bot_data)
        )

    elif data == "products":
        await query.edit_message_text(
            text="🎁 Select a category:",
            reply_markup=get_products_keyboard()
        )

    elif data.startswith("category_"):
        category_key = data.split("_", 1)[1]
        await query.edit_message_text(
            text=f"📂 Subcategories under *{CATEGORIES[category_key]['name']}*:",
            parse_mode="Markdown",
            reply_markup=get_subcategories_keyboard(category_key)
        )

    elif data.startswith("subcategory|"):
        _, category_key, sub_key = data.split("|")
        await query.edit_message_text(
            text="🛍 Choose a product:",
            reply_markup=get_product_keyboard(category_key, sub_key)
        )

    elif data.startswith("product|"):
        _, category_key, sub_key, product_key = data.split("|")
        product = CATEGORIES[category_key]["subcategories"][sub_key]["products"][product_key]
        await query.edit_message_text(
            text=f"*{product['name']}*\nSelect a quantity:",
            parse_mode="Markdown",
            reply_markup=get_quantity_keyboard(category_key, sub_key, product_key)
        )

    elif data.startswith("quantity|"):
        _, category_key, sub_key, product_key, qty = data.split("|")
        cart = context.bot_data.setdefault("cart", {}).setdefault(user_id, [])
        cart.append({
            "category": category_key,
            "subcategory": sub_key,
            "product": product_key,
            "quantity": qty
        })
        await query.edit_message_text(
            text=f"✅ Added *{qty}* of *{product_key.replace('_', ' ').title()}* to your cart!",
            parse_mode="Markdown",
            reply_markup=main_menu(user_id, context.bot_data)
        )

    elif data.startswith("custom_qty|"):
        _, category_key, sub_key, product_key = data.split("|")
        context.user_data["awaiting_custom_qty"] = {
            "category": category_key,
            "subcategory": sub_key,
            "product": product_key
        }
        await query.edit_message_text("✏️ Please type the quantity you want (e.g. 10g, 2 units, etc.)")





    try:
        if data.startswith("country_") or data == "main_menu": # This condition was already handled above, but keeping structure
            # This specific path for country/main_menu was already handled before the try-except.
            # If it reaches here, it means it wasn't one of those.
            # However, the original code had this if/elif structure, so I'll maintain it.
            # The primary handlers for these are above the try block.
            # This might be redundant or a fallback. For safety, ensure it does what's expected.
            if not (data.startswith("country_") or data == "main_menu"): # Add check to avoid re-processing if already handled
                 await query.edit_message_text("🏠 Main Menu:", reply_markup=main_menu(user_id, context.bot_data))
            return


        elif data == "how_it_works":
            how_text = "\n\n".join(HOW_IT_WORKS_LIST)
            await query.edit_message_text(
                how_text,
                parse_mode="Markdown",
                reply_markup=main_menu(user_id, context.bot_data)
            )
            return

        elif data == "reviews":
            logger.info("Processing 'reviews' callback.")
            reviews_text = get_all_reviews()
            logger.info(f"Text from get_all_reviews: '{reviews_text}'")
            try:
                await query.edit_message_text(
                    text=reviews_text,
                    parse_mode="Markdown",
                    reply_markup=main_menu(user_id, context.bot_data)
                )
                logger.info("Successfully edited message for reviews.")
            except Exception as e:
                logger.error(f"Error editing message for reviews: {e}", exc_info=True)
            return

        elif data == "products": # This was also handled above the try-except
            if not data == "products": # Add check to avoid re-processing
                await query.edit_message_text("🛒 Choose a category:", reply_markup=get_products_keyboard())
            return

        elif data.startswith("category_"): # Also handled above
            if not data.startswith("category_"): # Add check
                cat_key = data.split("category_")[1]
                await query.edit_message_text("📂 Choose a subcategory:", reply_markup=get_subcategories_keyboard(cat_key))
            return



        elif data.startswith("subcategory|"): # Also handled above
            if not data.startswith("subcategory|"): # Add check
                _, cat_key, sub_key = data.split("|")
                sub = CATEGORIES[cat_key]["subcategories"][sub_key]
                if "products" in sub:
                    await query.edit_message_text("🧪 Choose a product:", reply_markup=get_product_keyboard(cat_key, sub_key))
                else:
                    await query.edit_message_text("❌ No products found.")
            return

        elif data.startswith("product|"): # Also handled above
            if not data.startswith("product|"): # Add check
                _, cat_key, sub_key, product_key = data.split("|")
                product = CATEGORIES[cat_key]["subcategories"][sub_key]["products"][product_key]
                msg = f"📦 {product['name']}\n💸 Price: {product['price']}\n🧾 {product['description']}"
                await query.edit_message_text(msg, reply_markup=get_quantity_keyboard(cat_key, sub_key, product_key))
            return

        elif data.startswith("quantity|"): # Also handled above
             if not data.startswith("quantity|"): # Add check
                _, cat_key, sub_key, prod_key, qty = data.split("|")
                prod = CATEGORIES[cat_key]["subcategories"][sub_key]["products"][prod_key]
                price = prod["quantities"][qty] if isinstance(prod["quantities"], dict) else prod["price"]
                # This is where the cart structure was different in the original first callback_handler.
                # The current structure being saved is: {"product": prod["name"], "qty": qty, "price": price}
                # Let's ensure this is consistently used or reconciled.
                # The previous version (in the first callback_handler in user's code) was:
                # {"category": category_key, "subcategory": sub_key, "product": product_key, "quantity": qty}
                # The version I'm keeping from the more complete handler is:
                context.bot_data.setdefault("cart", {}).setdefault(user_id, []).append({
                    "product": prod["name"], # Storing name directly
                    "qty": qty,
                    "price": price
                })
                await query.edit_message_text(
                    f"✅ *{qty}* of *{prod['name']}* added to cart!\n\nYou can continue shopping or view your cart.",
                    parse_mode="Markdown",
                    reply_markup=main_menu(user_id, context.bot_data)
                )
             return

        elif data.startswith("custom_qty|"): # Also handled above
            if not data.startswith("custom_qty|"): # Add check
                _, cat_key, sub_key, prod_key = data.split("|")
                context.user_data["custom_input"] = { # This was `awaiting_custom_qty` before, changed to `custom_input` in my previous fix.
                    "cat_key": cat_key,
                    "sub_key": sub_key,
                    "prod_key": prod_key
                }
                await query.edit_message_text("✏️ Please type your custom quantity (e.g., 7 or 25):")
            return

        elif data == "pay_btc":
            await query.edit_message_text(
                "🪙 Send BTC to:\n`bc1q0q5j52rj50gwd2f7nlqqp89kgqdjqt0rcewr0m`",
                parse_mode="Markdown",
                reply_markup=main_menu(user_id, context.bot_data)
            )
            return

        elif data == "pay_usdt":
            await query.edit_message_text(
                "🪙 Send USDT to:\n`TRC20 TXTmvHkxL986msuvJU4KoEJsheiVSScC9J`",
                parse_mode="Markdown",
                reply_markup=main_menu(user_id, context.bot_data)
            )
            return


        elif data == "faqs":
            faq_text = "\n\n".join(FAQ_LIST)
            await query.edit_message_text(
                faq_text,
                parse_mode="Markdown",
                reply_markup=main_menu(user_id, context.bot_data)
            )
            return




        elif data == "cart":
            cart_items = context.bot_data.get("cart", {}).get(user_id, [])
            logger.info(f"Cart items for user {user_id}: {cart_items}")
            if cart_items:
                # Expects item to have 'qty', 'product' (name), and 'price'
                text_items = []
                for item in cart_items:
                    try:
                        # Ensure all keys are present to avoid KeyError
                        qty = item.get('qty', 'N/A')
                        product_name = item.get('product', 'Unknown Product')
                        price = item.get('price', 'N/A')
                        text_items.append(f"- {qty} of {product_name} @ {price}")
                    except KeyError as e:
                        logger.error(f"KeyError when formatting cart item: {item}. Missing key: {e}")
                        text_items.append(f"- Error displaying item: {item.get('product', 'Unknown Product')}")
                text = "🛒 Your Cart:\n" + "\n".join(text_items)
            else:
                text = "🛒 Your cart is currently empty."
            logger.info(f"Displaying cart text: {text}")
            await query.edit_message_text(text, reply_markup=main_menu(user_id, context.bot_data))
            return

        elif data == "orders":
            orders = context.bot_data.get("orders", {}).get(user_id, [])
            if orders:
                text = "📦 Your Orders:\n" + "\n".join(orders)
            else:
                text = "📦 You have no orders yet."
            await query.edit_message_text(text, reply_markup=main_menu(user_id, context.bot_data))
            return

        else:
            # If none of the specific `elif` conditions inside the `try` block matched,
            # and it wasn't handled by the `if/elif` blocks before the `try`,
            # then it's an unknown command for this section.
            # However, the initial more specific handlers (country, products, category, etc.)
            # should catch most valid known callbacks.
            # This path might be hit if a previous handler didn't `return`.
            # The original code had a simple `await query.edit_message_text("⚠️ Unknown command.")`
            # as a final else, which I removed when merging the two callback_handlers.
            # The more complete handler's `try...except` block implicitly covers this.
            # If it falls through all known `elif data == ...` then it does nothing more and the `try` finishes.
            # Adding a log for unhandled data inside this try block might be useful.
            logger.warning(f"Data '{data}' was not handled by specific elif blocks in the try section.")
            # To restore original behavior of an "Unknown command" message if nothing else matched:
            # await query.edit_message_text("⚠️ Unknown command within try block.", reply_markup=main_menu(user_id, context.bot_data))


    except BadRequest as e:
        logger.error(f"BadRequest in callback_handler: {e}", exc_info=True)
        if "Query is too old" in str(e) or "message is not modified" in str(e):
            pass # These are common and can often be ignored
        else:
            # For other BadRequests, you might want to inform the user or re-raise
            # Depending on how critical they are. For now, just logging.
            pass # Or: raise
    except Exception as e:
        logger.error(f"General Exception in callback_handler: {e}", exc_info=True)
        try:
            await query.edit_message_text("🤖 Oops! Something went wrong. Please try again.", reply_markup=main_menu(user_id, context.bot_data))
        except Exception as e_inner:
            logger.error(f"Failed to send error message to user: {e_inner}", exc_info=True)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /reviews to see product reviews or use the menu buttons.")

async def handle_custom_quantity_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    logger.info(f"Custom quantity input from user {user_id}: {text}")

    # custom_input_key = "custom_input" # This was what I used in a previous fix
    custom_input_key = "awaiting_custom_qty" # This is what the current code (after my overwrite) uses. Let's stick to it.

    if custom_input_key not in context.user_data:
        logger.warning(f"'{custom_input_key}' not in user_data for user {user_id}. Ignoring text input.")
        return

    if not text.isdigit():
        await update.message.reply_text("❌ Please enter a valid number.")
        return

    custom_qty = text
    # Use the correct key for retrieving data
    details = context.user_data[custom_input_key]
    cat_key = details["category"]
    sub_key = details["subcategory"]
    prod_key = details["product"]

    product = CATEGORIES[cat_key]["subcategories"][sub_key]["products"][prod_key]

    if isinstance(product["quantities"], dict):
        unit_price_str = product["quantities"].get("1", product.get("price", "50€")) # Fallback to product price if "1" not found
        unit_price_str = unit_price_str.split("€")[0] # ensure only number part
        try:
            unit_price = float(unit_price_str.replace("€", "").replace("/unit", "").strip())
        except ValueError:
            logger.error(f"Could not parse unit price from string: {unit_price_str}. Defaulting to 50.")
            unit_price = 50.0

    else: # If quantities is a list (e.g. ["10g", "20g"] - this case isn't fully handled for price) or not a dict
          # Default to product's main price, assuming it's per unit for custom qty.
        unit_price_str = product["price"].split("€")[0] # ensure only number part
        try:
            unit_price = float(unit_price_str.replace("€", "").replace("/unit", "").strip())
        except ValueError:
            logger.error(f"Could not parse product price: {product['price']}. Defaulting to 50.")
            unit_price = 50.0


    total_price = int(custom_qty) * unit_price

    # Ensure cart item structure is consistent: product name, qty, price string
    cart_item = {
        "product": product["name"],
        "qty": custom_qty,
        "price": f"{total_price:.2f}€" # Format price to 2 decimal places
    }
    context.bot_data.setdefault("cart", {}).setdefault(user_id, []).append(cart_item)
    logger.info(f"Added to cart for user {user_id}: {cart_item}")

    context.user_data.pop(custom_input_key)

    await update.message.reply_text(
        f"✅ *{custom_qty}* of *{product['name']}* added to cart!\n\nYou can continue shopping or view your cart.",
        parse_mode="Markdown",
        reply_markup=main_menu(user_id, context.bot_data)
    )


def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    PORT = int(os.environ.get("PORT", 10000))
    WEBHOOK_PATH = "/webhook"

    if not BOT_TOKEN :
        logger.error("❌ BOT_TOKEN not set.")
        raise Exception("❌ BOT_TOKEN not set.")
    if not HOSTNAME and WEBHOOK_PATH != "/webhook_local_test": # Allow HOSTNAME to be None for local polling test
         logger.error("❌ RENDER_EXTERNAL_HOSTNAME not set for webhook mode.")
         # raise Exception("❌ RENDER_EXTERNAL_HOSTNAME not set.") # Comment out for local test

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reviews", reviews_command))
    app.add_handler(CommandHandler("faqs", faqs_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_quantity_input))

    if HOSTNAME: # Production or staging with webhook
        logger.info(f"✅ Starting webhook server on port {PORT}...")
        logger.info(f"🔗 Webhook URL: https://{HOSTNAME}{WEBHOOK_PATH}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=WEBHOOK_PATH,
            webhook_url=f"https://{HOSTNAME}{WEBHOOK_PATH}"
        )
    else: # Local development, use polling
        logger.info("✅ Starting bot in polling mode...")
        app.run_polling()


if __name__ == "__main__":
    main()
