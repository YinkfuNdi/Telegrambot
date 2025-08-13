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
from telegram.error import BadRequest

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
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "60.00€" }
                },
                "purple_panties": {
                    "name": "Purple Panties - Indica - 2g",
                    "price": "60€/unit",
                    "description": "Purple Panties is a potent indica strain that soothes the body and calms the mind. Rich in flavor with sweet berry undertones.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "60.00€" }
                },
                "galactic_gas": {
                    "name": "Galactic Gas - Indica - 2g",
                    "price": "60€/unit",
                    "description": "Galactic Gas delivers a cosmic indica high with deep relaxation and pungent earthy notes. Perfect for night use.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "60.00€" }
                },
                "lime_sherbert": {
                    "name": "Lime Sherbert - Hybrid - 2g",
                    "price": "60€/unit",
                    "description": "Lime Sherbert offers a citrusy twist on hybrid relaxation. Energizing and soothing with a tart lime finish.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "60.00€" }
                },
                "caribbean_crush": {
                    "name": "Caribbean Crush - Sativa - 2g",
                    "price": "60€/unit",
                    "description": "Caribbean Crush is a vibrant sativa with tropical notes and uplifting effects, perfect for social and creative sessions.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "60.00€" }
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
                    "name": "Dosi Rocky Runtz - Indica - 2g", "price": "70€/unit",
                    "description": "Dosi Rocky Runtz delivers a deeply relaxing indica buzz with sweet earthy tones. Great for evening unwind and sleep.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "70.00€" }
                },
                "kosmic_kiwi": {
                    "name": "Kosmic Kiwi - Hybrid - 2g", "price": "70€/unit",
                    "description": "Kosmic Kiwi is a hybrid vape with 2000mg of potent blend. Enjoy smooth hits and long-lasting satisfaction with fruity freshness.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "70.00€" }
                },
                "straw_sherb": {
                    "name": "Strawberry Sherbet - Hybrid - 2g", "price": "70€/unit",
                    "description": "Strawberry Sherbet delivers sweet creamy hits with balanced hybrid effects. Relaxing and uplifting all in one.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "70.00€" }
                },
                "face_punch": {
                    "name": "Tropical Face Punch - Sativa - 2g", "price": "70€/unit",
                    "description": "Tropical Face Punch hits with energetic tropical flavor and a bold sativa kick. Great for a morning boost.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "70.00€" }
                },
                "apple_sour": {
                    "name": "Glazed Apple Sour - Sativa - 2g", "price": "70€/unit",
                    "description": "Glazed Apple Sour is a sativa blend with sweet and sour green apple notes. Stimulating and flavorful vape experience.",
                    "quantities": { "50": "45.00€", "20": "50.00€", "5": "55.00€", "1": "70.00€" }
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
                        "name": "Love Affair - Sativa - 2g", "price": "60€/unit",
                        "description": "Watermelon Gelato is a flavorful indica strain known for its sweet, fruity aroma and ultra-smooth smoke. Bursting with notes of watermelon, berries, and creamy gelato undertones, it delivers a calming body high that's perfect for relaxation, stress relief, and peaceful evenings. Ideal for unwinding without heavy sedation, this strain combines flavor with tranquility.",
                        "quantities": { "50": "35.00€", "20": "40.00€", "5": "45.00€", "1": "50.00€" }
                    },
                    "peach_cresc": {
                        "name": "Peach Crescendo - Sativa - 2g", "price": "60€/unit",
                        "description": "Peach Crescendo is a vibrant sativa strain that bursts with the juicy flavor of ripe peaches blended with subtle tropical and citrus notes. Known for its uplifting and energizing effects, it sparks creativity and mental clarity while keeping the body light and active. Ideal for daytime use, social settings, or creative sessions, this strain is a flavorful way to boost your mood and motivation.",
                        "quantities": { "1": "60.00€" }
                    },
                    "trop_burst": {
                        "name": "Tropical Burst - Sativa - 2g", "price": "60€/unit",
                        "description": "Tropical Burst is a zesty sativa strain packed with a medley of exotic fruit flavors, including mango, pineapple, and papaya. Its aroma is equally enticing, delivering a sweet and tangy scent with a refreshing, clean finish. Known for its uplifting and energizing high, Tropical Burst enhances focus and creativity, making it perfect for daytime adventures, productivity, or a vibrant social buzz.",
                        "quantities": { "1": "60.00€" }
                    },
                    "blue_lob": {
                        "name": "Blue Lobstar - Sativa - 2g", "price": "60€/unit",
                        "description": "Blue Lobstar is a rare and flavorful sativa strain that combines sweet blueberry notes with a citrus-forward punch, creating a vibrant and refreshing experience. Its aroma is fruity and tangy, with hints of lemon zest and herbal undertones. Known for delivering a smooth cerebral buzz, this strain boosts mental clarity and creativity while keeping the body light and relaxed—ideal for daytime use or social occasions.",
                        "quantities": { "1": "60.00€" }
                    },
                    "crunch_berry": {
                        "name": "Crunch Berries - Sativa - 2g", "price": "60€/unit",
                        "description": "Berry-rich and uplifting.", "quantities": { "1": "60.00€" }
                    }
                }
            },
            "indica": {
                "name": "Indica - 2g",
                "products": {
                    "cadi_rain": {
                        "name": "Cadillac Rainbow - Indica - 2g", "price": "60€/unit",
                        "description": "Cadillac Rainbow is a potent indica strain celebrated for its deeply relaxing effects and vibrant terpene profile. With a rich aroma of berries, earthy pine, and a hint of sweet diesel, this strain delivers a full-bodied experience that calms the mind and soothes the body. Its multicolored buds and thick resin production reflect its premium quality. Ideal for evening use, stress relief, and deep sleep, Cadillac Rainbow wraps you in a luxurious sense of tranquility.",
                        "quantities": { "1": "60.00€" }
                    }
                }
            },
            "hybrid": {
                "name": "Hybrid - 2g",
                "products": {
                    "cherry_pie": {
                        "name": "Cherry Pie OG - Hybrid - 2g", "price": "60€/unit",
                        "description": "Cherry Pie OG is a well-balanced hybrid strain known for its sweet and tart cherry aroma layered with hints of earthy spice. Its dense, trichome-covered buds deliver a calming yet uplifting experience, making it great for both daytime relaxation and evening unwinding. With genetics that combine Granddaddy Purple and Durban Poison, Cherry Pie OG offers a euphoric mental buzz followed by gentle body relaxation, perfect for relieving stress, anxiety, and mild aches.",
                        "quantities": { "1": "60.00€" }
                    },
                    "candy_rain": {
                        "name": "Candy Rain - Hybrid - 2g", "price": "60€/unit",
                        "description": "Candy Rain is a delightful hybrid strain with a sweet, sugary aroma reminiscent of freshly fallen candy. Known for its smooth and relaxing effects, it offers a gentle balance of uplifting mental clarity and soothing body calm. Perfect for easing stress and promoting relaxation without heavy sedation, Candy Rain is ideal for daytime use or unwinding after a long day.",
                        "quantities": { "1": "60.00€" }
                    },
                    "apples_ban": {
                        "name": "Apples & Banana's - Hybrid - 2g", "price": "60€/unit",
                        "description": "Apples & Banana's is a flavorful hybrid strain that blends sweet fruity notes of crisp apples and ripe bananas. It delivers a well-balanced experience, combining a gentle cerebral uplift with relaxing body sensations. Ideal for enhancing creativity and mood while keeping you calm and focused, this strain is perfect for both social occasions and quiet relaxation.",
                        "quantities": { "1": "60.00€" }
                    },
                    "blue_cake": {
                        "name": "Blueberry Cupcake - Hybrid - 2g", "price": "60€/unit",
                        "description": "Blueberry Cupcake is a delightful hybrid strain that combines sweet blueberry flavors with a smooth, mellow effect. Known for its relaxing yet uplifting qualities, it provides a gentle cerebral buzz paired with soothing body relaxation. Perfect for unwinding after a long day or enhancing creative activities, this strain offers a deliciously sweet aroma and taste reminiscent of freshly baked cupcakes.",
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
        {"stars": 4, "text": "Good focus, but a bit dry."}
    ],
    "double_bubble": [
        {"stars": 4, "text": "Sweet and fun, good hybrid."},
        {"stars": 5, "text": "Exactly like the candy, amazing buzz!"}
    ],
    "snoop_og": [
        {"stars": 5, "text": "True OG vibes, super relaxing for evenings."},
        {"stars": 4, "text": "Potent stuff, definitely an indica knockout."}
    ],
    "golden_pineapple": [
        {"stars": 5, "text": "So fruity and uplifting, great for creativity!"}
    ],
    "kosmic_kiwi": [ # From Hidden Hills
        {"stars": 4, "text": "Smooth vape, interesting kiwi flavor. Nice hybrid effects."}
    ],
    "peach_cresc": [ # From t10b2g
        {"stars": 5, "text": "The peach flavor is incredible. Really energizing."}
    ]
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
        logger.warning(f"Product {product_key} quantities is not a dict: {quantities}. Using product price.")
        pass

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
    logger.info(f"Accessing REVIEWS dictionary: {REVIEWS}")
    if not REVIEWS:
        logger.warning("REVIEWS dictionary is empty or not defined properly.")
        return "No reviews available at the moment."

    review_texts = []
    try:
        for product_key, reviews_list in REVIEWS.items():
            product_name_display = product_key.replace('_', ' ').title()
            found_product = False
            for cat_data in CATEGORIES.values():
                for sub_cat_data in cat_data.get("subcategories", {}).values():
                    if product_key in sub_cat_data.get("products", {}):
                        product_name_display = sub_cat_data["products"][product_key]["name"]
                        found_product = True
                        break
                if found_product:
                    break

            review_texts.append(f"📦 *{product_name_display}* Reviews:\n")
            if isinstance(reviews_list, list):
                for review in reviews_list:
                    if isinstance(review, dict) and "stars" in review and "text" in review:
                        stars = "⭐" * review["stars"]
                        review_texts.append(f"{stars} {review['text']}")
                    else:
                        logger.error(f"Malformed review item for product {product_key}: {review}")
                        review_texts.append(f"_Error displaying a review for {product_name_display}_")
            else:
                logger.error(f"Malformed reviews list for product {product_key}: {reviews_list}")
                review_texts.append(f"_Error displaying reviews for {product_name_display}_")
            review_texts.append("")
    except Exception as e:
        logger.error(f"Error in get_all_reviews: {e}", exc_info=True)
        return "An error occurred while fetching reviews."

    if not review_texts:
        logger.info("No review texts were generated, REVIEWS might be empty or all items malformed.")
        return "No reviews found."
    return "\n".join(review_texts)

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Command /start received from user {update.effective_user.id}")
    welcome_message = \"\"\"
Welcome to The 10/10 Boys self-service vape shop 🍃.

Ships From/To: United Kingdom 🇬🇧 / 🇪🇺 European Union⚡️🚚
Currency: GBP / EUR 💷💶
Currently Accepting: Crypto (USDT),(BTC),
﹎﹎﹎﹎﹎﹎﹎
Start with Help! /help and /userguide 📘.
Type /menu then click Products (Button) or just type in /products 📦.
Type /coupons to find discount codes 💰.Happy shopping
Note: For Spain and Portugal we ship to Mainland and islands.

Peace and Love ✌️❤️
The 10/10 Boys ®️
Telegram Support: @The1010Boysla
\"\"\"
    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        "🌍 Please select your country:",
        reply_markup=get_country_keyboard()
    )

async def reviews_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"Command /reviews received from user {user_id}")
    await update.message.reply_text(
        get_all_reviews(),
        parse_mode="Markdown",
        reply_markup=main_menu(user_id, context.bot_data)
    )
    
async def faqs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"Command /faqs received from user {user_id}")
    faq_text = "\n\n".join(FAQ_LIST)
    await update.message.reply_text(
        faq_text,
        parse_mode="Markdown",
        reply_markup=main_menu(user_id, context.bot_data)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"Command /help received from user {user_id}")
    await update.message.reply_text(
        "Welcome to the Help section!\n\n"
        "Here's how to use the bot:\n"
        "- Use /start to begin and select your country.\n"
        "- Click '🎁 Products' to browse items.\n"
        "- Add items to your '🛒 Cart'.\n"
        "- View '📦 Orders' for your past orders (if any).\n"
        "- Check '❓ FAQs' for common questions.\n"
        "- See '📊 Reviews' for product feedback.\n\n"
        "If you need further assistance, please describe your issue.",
        reply_markup=main_menu(user_id, context.bot_data)
    )

# --- Callback Handler ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except Exception as e:
        logger.error(f"Failed to answer callback query (ID: {query.id}): {e}", exc_info=True)

    data = query.data
    user_id = update.effective_user.id
    
    logger.info(f"Callback query received: Data='{data}', UserID={user_id}, QueryID={query.id}")

    try:
        if data.startswith("country_"):
            country = data.split("_", 1)[1].replace('_', ' ')
            context.user_data["country"] = country
            logger.info(f"User {user_id} selected country: {country}")
            await query.edit_message_text(
                text=f"✅ You selected *{country}*.\nHere is the main menu:",
                parse_mode="Markdown",
                reply_markup=main_menu(user_id, context.bot_data)
            )
        elif data == "main_menu":
            logger.info(f"User {user_id} requested main menu.")
            await query.edit_message_text(
                text="🏠 Main Menu:",
                reply_markup=main_menu(user_id, context.bot_data)
            )
        elif data == "products":
            logger.info(f"User {user_id} requested product categories.")
            await query.edit_message_text(
                text="🎁 Select a category:",
                reply_markup=get_products_keyboard()
            )
        elif data.startswith("category_"):
            category_key = data.split("_", 1)[1]
            logger.info(f"User {user_id} selected category: {category_key}")
            await query.edit_message_text(
                text=f"📂 Subcategories under *{CATEGORIES[category_key]['name']}*:",
                parse_mode="Markdown",
                reply_markup=get_subcategories_keyboard(category_key)
            )
        elif data.startswith("subcategory|"):
            _, category_key, sub_key = data.split("|")
            logger.info(f"User {user_id} selected subcategory: {category_key}|{sub_key}")
            await query.edit_message_text(
                text="🛍 Choose a product:",
                reply_markup=get_product_keyboard(category_key, sub_key)
            )
        elif data.startswith("product|"):
            _, category_key, sub_key, product_key = data.split("|")
            product = CATEGORIES[category_key]["subcategories"][sub_key]["products"][product_key]
            logger.info(f"User {user_id} selected product: {product_key}")
            msg = f"📦 *{product['name']}*\n💸 Price: {product['price']}\n\n{product['description']}\n\nSelect a quantity:"
            await query.edit_message_text(
                text=msg,
                parse_mode="Markdown",
                reply_markup=get_quantity_keyboard(category_key, sub_key, product_key)
            )
        elif data.startswith("quantity|"):
            _, category_key, sub_key, product_key, qty_selected = data.split("|")
            product_data = CATEGORIES[category_key]["subcategories"][sub_key]["products"][product_key]

            item_price_str = product_data["quantities"].get(qty_selected, product_data["price"]) if isinstance(product_data["quantities"], dict) else product_data["price"]

            cart_item = {
                "product": product_data["name"],
                "qty": qty_selected,
                "price": item_price_str
            }
            context.bot_data.setdefault("cart", {}).setdefault(user_id, []).append(cart_item)
            logger.info(f"User {user_id} added to cart: {cart_item}")
            await query.edit_message_text(
                text=f"✅ Added *{qty_selected}* of *{product_data['name']}* to your cart!\n\nYou can continue shopping or view your cart.",
                parse_mode="Markdown",
                reply_markup=main_menu(user_id, context.bot_data)
            )
        elif data.startswith("custom_qty|"):
            _, category_key, sub_key, product_key = data.split("|")
            context.user_data["awaiting_custom_qty"] = {
                "category": category_key, "subcategory": sub_key, "product": product_key
            }
            logger.info(f"User {user_id} requesting custom quantity for product: {product_key}")
            await query.edit_message_text("✏️ Please type the quantity you want (e.g., 10 or 2):")

        elif data == "how_it_works":
            logger.info(f"User {user_id} requested 'how_it_works'.")
            await query.edit_message_text("\n\n".join(HOW_IT_WORKS_LIST), parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))
        elif data == "reviews":
            logger.info(f"User {user_id} requested 'reviews'.")
            await query.edit_message_text(get_all_reviews(), parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))
        elif data == "faqs":
            logger.info(f"User {user_id} requested 'faqs'.")
            await query.edit_message_text("\n\n".join(FAQ_LIST), parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))
        elif data == "cart":
            cart_items = context.bot_data.get("cart", {}).get(user_id, [])
            logger.info(f"User {user_id} requested 'cart'. Items: {cart_items}")
            text_items = []
            if cart_items:
                for item in cart_items:
                    qty = item.get('qty', 'N/A')
                    product_name = item.get('product', 'Unknown Product')
                    price = item.get('price', 'N/A')
                    text_items.append(f"- {qty} of {product_name} @ {price}")
                text_to_send = "🛒 Your Cart:\n" + "\n".join(text_items)
            else:
                text_to_send = "🛒 Your cart is currently empty."
            await query.edit_message_text(text_to_send, reply_markup=main_menu(user_id, context.bot_data))

        elif data == "orders":
            logger.info(f"User {user_id} requested 'orders'.")
            # Updated "Orders" text
            orders_text = "📦 *Your Orders*\n\nCurrently, you have no past orders displayed here. Once you complete a purchase, it will appear in this section.\n\nIf you believe you have past orders that aren't showing, please contact support (details to be provided)."
            await query.edit_message_text(orders_text, parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))

        elif data == "user_guide":
            logger.info(f"User {user_id} requested 'user_guide'.")
            user_guide_text = """*📘 User Guide: Placing Your Order*

Ordering with us is simple! Follow these steps:

1️⃣ *Select Your Country:*
   - If you haven't already, use the `/start` command and choose your country from the list.

2️⃣ *Browse Products:*
   - Tap the "🎁 Products" button on the main menu.
   - Select a product category (e.g., "The 10/10 Boys").
   - Choose a subcategory (e.g., "The 10/10 Boys - 1g").
   - Tap on the product you're interested in.

3️⃣ *Choose Quantity:*
   - You'll see product details and available quantities with prices.
   - Tap a predefined quantity button (e.g., "1 - 50.00€").
   - *Alternatively*, tap "✏️ Enter Custom Quantity" and then type your desired amount in grams or units when prompted (e.g., type "3").

4️⃣ *Add to Cart:*
   - After selecting a quantity, the item is automatically added to your cart.
   - You'll see a confirmation and be returned to the main menu.

5️⃣ *Review Your Cart:*
   - Tap "🛒 Cart (X)" on the main menu at any time to see what you've added.

6️⃣ *Proceed to Payment:*
   - After adding items, you can click on "🛒 Cart" and then choose a payment option if available, or follow prompts for payment (e.g., BTC/USDT).

Happy shopping!"""
            await query.edit_message_text(user_guide_text, parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))

        elif data == "ref_earn":
            logger.info(f"User {user_id} requested 'ref_earn'.")
            ref_earn_text = """*📢 Refer & Earn*

Our referral program is currently under development! We're working on exciting ways for you to earn rewards by sharing our products with your friends.

Stay tuned for updates on how you can benefit from spreading the word!"""
            await query.edit_message_text(ref_earn_text, parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))

        elif data == "coupon":
            logger.info(f"User {user_id} requested 'coupon'.")
            coupon_text = """*🏷️ Coupons & Promotions*

We love giving back to our community!
Keep an eye on our announcements for special promotions, discounts, and coupon codes that you can use with your orders.

Currently, all available prices are listed with the products. If a coupon system is implemented, you'll typically apply codes at a checkout stage."""
            await query.edit_message_text(coupon_text, parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))

        elif data == "friendly_services":
            logger.info(f"User {user_id} requested 'friendly_services'.")
            friendly_services_text = """*❤️ Friendly Services*

We're committed to providing you with a great experience! Here are some of the friendly services we aim to offer:

✅ *Quality Products:* A curated selection of high-quality items.
✅ *Discreet Shipping:* Your privacy is important to us. All orders are packaged and shipped discreetly.
✅ *Clear Information:* We aim to provide clear details about our products and how to order via our User Guide and FAQs.
✅ *Support:* If you have questions, our '❓ FAQs' or '✋ Help' sections are your first stop.

Your satisfaction is our priority!"""
            await query.edit_message_text(friendly_services_text, parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))

        elif data == "help":
            logger.info(f"User {user_id} clicked help button.")
            help_button_text = """*✋ Bot Help & Navigation*

Here's a quick guide to the main menu buttons:

🤔 *How does it work?:* General overview of the bot's process.
📘 *User Guide:* Step-by-step instructions on placing an order.
🎁 *Products:* Browse and select items from our categories.
📊 *Reviews:* See what others say about our products.
📢 *Ref & Earn:* Info about our upcoming referral program.
🏷 *Coupon:* Details about promotions.
❤️ *Friendly Services:* Learn about our commitment to you.
❓ *FAQs:* Find answers to frequently asked questions.
🛒 *Cart (X):* View and manage items you've added.
📦 *Orders (X):* Check your order history (coming soon).

Use these buttons to navigate. If you get stuck, try returning to the /start menu or use the /help command for a general command list."""
            await query.edit_message_text(help_button_text, parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))

        elif data == "pay_btc":
            logger.info(f"User {user_id} chose Pay with BTC.")
            await query.edit_message_text("🪙 Send BTC to:\n`bc1q0q5j52rj50gwd2f7nlqqp89kgqdjqt0rcewr0m`", parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))
        elif data == "pay_usdt":
            logger.info(f"User {user_id} chose Pay with USDT.")
            await query.edit_message_text("🪙 Send USDT to:\n`TRC20 TXTmvHkxL986msuvJU4KoEJsheiVSScC9J`", parse_mode="Markdown", reply_markup=main_menu(user_id, context.bot_data))
        else:
            logger.warning(f"Unhandled callback data '{data}' for user {user_id}.")
            await query.edit_message_text("⚠️ Unknown command or action.", reply_markup=main_menu(user_id, context.bot_data))

    except BadRequest as e:
        logger.error(f"BadRequest in callback_handler for data '{data}', user {user_id}, QueryID {query.id}: {e}", exc_info=True)
        if "message is not modified" not in str(e).lower() and "query is too old" not in str(e).lower():
            try:
                 await query.edit_message_text("🤖 Error processing your request. Please try again.", reply_markup=main_menu(user_id, context.bot_data))
            except Exception as e_inner:
                 logger.error(f"Failed to send error message to user after BadRequest: {e_inner}", exc_info=True)
    except Exception as e:
        logger.error(f"General Exception in callback_handler for data '{data}', user {user_id}, QueryID {query.id}: {e}", exc_info=True)
        try:
            await query.edit_message_text("🤖 Oops! Something went terribly wrong. Please try again later.", reply_markup=main_menu(user_id, context.bot_data))
        except Exception as e_inner:
            logger.error(f"Failed to send generic error message to user: {e_inner}", exc_info=True)

# --- Message Handler for Custom Quantity ---
async def handle_custom_quantity_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text_input = update.message.text.strip()
    logger.info(f"Custom quantity input from user {user_id}: '{text_input}'")

    custom_qty_details_key = "awaiting_custom_qty"
    if custom_qty_details_key not in context.user_data:
        logger.warning(f"'{custom_qty_details_key}' not in user_data for user {user_id}. Ignoring text input: '{text_input}'")
        return

    if not text_input.isdigit() or int(text_input) <= 0:
        logger.warning(f"Invalid custom quantity '{text_input}' from user {user_id}.")
        await update.message.reply_text("❌ Please enter a valid positive number for the quantity.")
        return

    custom_qty_str = text_input
    details = context.user_data[custom_qty_details_key]
    cat_key, sub_key, prod_key = details["category"], details["subcategory"], details["product"]
    product_data = CATEGORIES[cat_key]["subcategories"][sub_key]["products"][prod_key]

    unit_price_val = 50.0
    price_source_str = product_data.get("price", "50€")
    if isinstance(product_data.get("quantities"), dict):
        price_source_str = product_data["quantities"].get("1", price_source_str)

    try:
        numeric_part = ''.join(filter(lambda x: x.isdigit() or x == '.', price_source_str.split('€')[0]))
        if numeric_part: unit_price_val = float(numeric_part)
        else: logger.error(f"Could not parse numeric part from '{price_source_str}' for {prod_key}. Defaulting to {unit_price_val}.")
    except ValueError:
        logger.error(f"ValueError parsing unit price from '{price_source_str}' for {prod_key}. Defaulting to {unit_price_val}.")

    total_price = int(custom_qty_str) * unit_price_val
    cart_item = {"product": product_data["name"], "qty": custom_qty_str, "price": f"{total_price:.2f}€"}

    context.bot_data.setdefault("cart", {}).setdefault(user_id, []).append(cart_item)
    logger.info(f"Added custom quantity to cart for user {user_id}: {cart_item}")
    context.user_data.pop(custom_qty_details_key)

    await update.message.reply_text(
        f"✅ *{custom_qty_str}* of *{product_data['name']}* (total {total_price:.2f}€) added to cart!\n\nYou can continue shopping or view your cart.",
        parse_mode="Markdown",
        reply_markup=main_menu(user_id, context.bot_data)
    )
    
# --- Main Application Setup ---
def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    PORT = int(os.environ.get("PORT", 10000))
    WEBHOOK_PATH = "/webhook"

    if not BOT_TOKEN:
        logger.critical("❌ BOT_TOKEN environment variable not set.")
        raise Exception("❌ BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reviews", reviews_command))
    app.add_handler(CommandHandler("faqs", faqs_command))
    app.add_handler(CommandHandler("help", help_command)) # For /help command
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_quantity_input))

    logger.info("Bot handlers registered.")

    if HOSTNAME:
        logger.info(f"Starting bot in webhook mode. Host: {HOSTNAME}, Port: {PORT}, Path: {WEBHOOK_PATH}")
        app.run_webhook(listen="0.0.0.0", port=PORT, url_path=WEBHOOK_PATH, webhook_url=f"https://{HOSTNAME}{WEBHOOK_PATH}")
    else:
        logger.info("Starting bot in polling mode for local development.")
        app.run_polling()

if __name__ == "__main__":
    main()
