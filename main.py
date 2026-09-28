import logging
import os

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


# ============================================
# INSTELLINGEN
# ============================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

# Je eigen site — vast ingesteld zodat de link niet stil gewijzigd kan worden.
SITE_URL = "https://www.lieteberg.be/nl"

PHONE_DISPLAY = "089 25 50 60"
EMAIL = "info@lieteberg.be"
ADDRESS = "Stalkerweg 46, 3690 Zutendaal"

# Optioneel — invullen om de knoppen te tonen (leeg = verborgen).
INSTAGRAM_URL = ""
FACEBOOK_URL = ""

BRAND = "Lieteberg"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============================================
# ONDERDELEN
# key -> (titel, beschrijving, [punten])
# ============================================
SECTIONS = {
    "blotevoetenpad": (
        "🦶 Blotevoetenpad",
        "Een natuurpad van zo'n 3 km dat je op blote voeten beleeft — avontuur en plezier "
        "voor jong én oud.",
        ["± 3 km op blote voeten", "Verschillende ondergronden", "Vanaf €6"],
    ),
    "biodrome": (
        "🔬 BioDrome",
        "Interactieve belevingstentoonstelling over biodiversiteit.",
        ["Interactief & leerrijk", "Voor het hele gezin", "Vanaf €7"],
    ),
    "vlindertuin": (
        "🦋 Vlindertuin",
        "Een bloemrijke tuin vol inheemse vlinders en bloeiende planten.",
        ["Inheemse vlinders", "Bloemrijke beplanting", "Rustig wandelen"],
    ),
    "bijen": (
        "🐝 Bestuivers",
        "Steunpunt Bijenteelt Limburg — alles over bijen en bestuivers.",
        ["Kenniscentrum bijenteelt", "Over bestuivers & natuur", "Educatief aanbod"],
    ),
    "groepen": (
        "👥 Groepen & workshops",
        "Begeleide groepsbezoeken en workshops op maat.",
        ["Rondleiding met gids", "Workshops", "Op afspraak"],
    ),
    "praktisch": (
        "ℹ️ Praktisch",
        "Handig om te weten tijdens je bezoek.",
        ["Fietsverhuur", "Bistro Lieteberg", "Lietebergshop (honing)", "Elke dag open vanaf 10 u"],
    ),
}

SECTION_ORDER = ["blotevoetenpad", "biodrome", "vlindertuin", "bijen", "groepen", "praktisch"]


# ============================================
# TEKSTEN
# ============================================
TEXT_START = (
    f"🌿 <b>{BRAND}</b>\n\n"
    "<i>Belevingscentrum Biodiversiteit in Zutendaal (Limburg): blotevoetenpad, "
    "BioDrome, vlindertuin en meer.</i>\n\n"
    "Ontdek het aanbod en reserveer je tickets op de website."
)

TEXT_SECTIONS = (
    "🌿 <b>Ontdek Lieteberg</b>\n\n"
    "Kies een onderdeel voor meer info. Tickets en openingstijden staan op de website."
)

TEXT_MENU = (
    "🗂 <b>Menu</b>\n\n"
    "• Bekijk het <b>aanbod</b> van Lieteberg.\n"
    "• Reserveer rechtstreeks op de website.\n"
    "• Lees de veelgestelde vragen.\n"
    "• Neem contact op."
)

TEXT_FAQ = (
    "❓ <b>Veelgestelde vragen</b>\n\n"
    "<b>Hoe reserveer ik?</b>\n"
    "Gebruik de knop om de website te openen: tickets, prijzen en openingstijden vind je "
    "daar. Bellen of mailen kan ook.\n\n"
    "<b>Wanneer zijn jullie open?</b>\n"
    "Elke dag open vanaf 10 u. Bekijk de website voor actuele uren en sluitingsdagen.\n\n"
    "<b>Is er parking?</b>\n"
    "Ja, er is parkeergelegenheid ter plaatse aan Stalkerweg 46.\n\n"
    "<b>Is het geschikt voor kinderen?</b>\n"
    "Zeker — het blotevoetenpad en de BioDrome zijn erg in trek bij gezinnen."
)

TEXT_CONTACT = (
    "✏️ <b>Contact</b>\n\n"
    f"• Telefoon: {PHONE_DISPLAY}\n"
    f"• E-mail: {EMAIL}\n"
    f"• Adres: {ADDRESS}\n\n"
    "Tickets en openingstijden staan het snelst op de website."
)

HIGHLIGHTS = "In het kort:"
BOOK_NOTE = "Tickets en openingstijden op de website."


# ============================================
# HULPFUNCTIES
# ============================================
def btn(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def url_btn(text, url):
    return types.InlineKeyboardButton(text=text, url=url)


def site_btn():
    return types.InlineKeyboardButton(text="🌐 Website", web_app=types.WebAppInfo(url=SITE_URL))


def book_btn():
    return types.InlineKeyboardButton(
        text="🎟 Tickets & reserveren", web_app=types.WebAppInfo(url=SITE_URL)
    )


def ig_btn():
    return url_btn("📸 Instagram", INSTAGRAM_URL) if INSTAGRAM_URL else None


def fb_btn():
    return url_btn("📘 Facebook", FACEBOOK_URL) if FACEBOOK_URL else None


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [b for b in row if b is not None]
        if row:
            markup.row(*row)
    return markup


BTN_SECTIONS = ("🌿 Ontdek", "sections")
BTN_MENU = ("🗂 Menu", "menu")


# ============================================
# SCHERM / KAART
# ============================================
def section_text(key):
    title, desc, items = SECTIONS[key]
    lines = "\n".join(f"• {i}" for i in items)
    return f"<b>{title}</b>\n\n{desc}\n\n<b>{HIGHLIGHTS}</b>\n{lines}\n\n<i>{BOOK_NOTE}</i>"


def section_rows(key):
    return [
        [book_btn()],
        [btn("‹ Terug naar aanbod", "sections"), btn(*BTN_MENU)],
    ]


def screen(action):
    if action in ("home", "start"):
        return TEXT_START, [
            [btn(*BTN_SECTIONS)],
            [book_btn()],
            [site_btn()],
            [ig_btn(), fb_btn()],
        ]
    if action == "sections":
        rows = [[btn(SECTIONS[k][0], f"sec:{k}")] for k in SECTION_ORDER]
        rows.append([btn(*BTN_MENU)])
        return TEXT_SECTIONS, rows
    if action == "menu":
        return TEXT_MENU, [
            [btn(*BTN_SECTIONS)],
            [btn("❓ FAQ", "faq"), btn("✏️ Contact", "contact")],
            [site_btn()],
            [ig_btn(), fb_btn()],
        ]
    if action == "faq":
        return TEXT_FAQ, [[btn(*BTN_SECTIONS)], [btn(*BTN_MENU)]]
    if action == "contact":
        return TEXT_CONTACT, [
            [book_btn()],
            [ig_btn(), fb_btn()],
            [btn(*BTN_SECTIONS), btn(*BTN_MENU)],
        ]
    return None


# ============================================
# HANDLERS
# ============================================
@bot.message_handler(commands=["start"])
def start(message):
    text, rows = screen("home")
    bot.send_message(message.chat.id, text, reply_markup=make_markup(rows))


def render(call, text, rows):
    markup = make_markup(rows)
    try:
        bot.edit_message_text(
            text, chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=markup,
        )
    except ApiTelegramException:
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("sec:"))
def show_section(call):
    bot.answer_callback_query(call.id)
    key = call.data.split(":", 1)[1]
    if key in SECTIONS:
        render(call, section_text(key), section_rows(key))


@bot.callback_query_handler(func=lambda call: True)
def show_screen(call):
    bot.answer_callback_query(call.id)
    result = screen(call.data)
    if result:
        render(call, result[0], result[1])


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    try:
        bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(
                type="web_app",
                text="Tickets",
                web_app=types.WebAppInfo(url=SITE_URL),
            )
        )
    except ApiTelegramException:
        pass

    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
