from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def country_menu():
    countries = [
        ("🇦🇹 Austria", "country_austria"),
        ("🇨🇭 Switzerland", "country_switzerland"),
        ("🇩🇪 Germany", "country_germany"),
        ("🇪🇸 Spain", "country_spain"),
        ("🇫🇷 France", "country_france"),
        ("🇬🇧 UK", "country_uk"),
        ("🇮🇹 Italy", "country_italy"),
        ("🇳🇱 Netherlands", "country_netherlands"),
        ("🇵🇹 Portugal", "country_portugal"),
    ]
    buttons = [[InlineKeyboardButton(name, callback_data=code)] for name, code in countries]
    return InlineKeyboardMarkup(buttons)
