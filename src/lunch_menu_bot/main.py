import logging
import random
from lunch_menu_bot.discord.bot import LunchMenuBot
from lunch_menu_bot.discord.embeds import (
    embed_confused,
    embed_fail,
    embed_chicken1,
    embed_chicken2,
    embed_chicken3,
)
from dotenv import dotenv_values
from lunch_menu_bot.format.openai import get_client, prettify, remove_empty_lines
from lunch_menu_bot.menu.kragerup_og_ko import fetch_menu_page, parse_menu_page
from lunch_menu_bot.time.time import get_week_and_day

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# load .env file
config = dotenv_values(".secrets")
DISCORD_BOT_TOKEN = config["DISCORD_BOT_TOKEN"]
DISCORD_CHANNEL_ID = config["DISCORD_CHANNEL_ID"]
OPENAI_API_KEY = config["OPENAI_API_KEY"]

openai_client = get_client(OPENAI_API_KEY)


def get_menu() -> str:
    logger.info("Fetching the menu...")
    html_content = fetch_menu_page()

    logger.info("Parsing the menu...")
    week_number, day = get_week_and_day()
    column_identifier = f"Uge {week_number}"
    menu = parse_menu_page(html_content, column_identifier)

    # Check validity
    if menu is None:
        logger.error("No menu found")
        return embed_fail
    if day not in menu:
        logger.warning("No menu found for today")
        return ("wtf no food today??", embed_confused)

    logger.info("Prettifying the menu...")

    menu_raw = menu[day]
    logger.info(f"Menu for {day}: {menu_raw}")

    menu_pretty = remove_empty_lines(prettify(openai_client, menu_raw))
    logger.info(f"Prettified menu for {day}: {menu_pretty}")

    embed = None
    if "hønsesalat" in menu_raw.lower():
        embed = random.choice([embed_chicken1, embed_chicken2, embed_chicken3])

    return menu_pretty if embed is None else (menu_pretty, embed)


logger.info("Starting the bot...")
bot = LunchMenuBot(func_get_menu=get_menu)
bot.run(DISCORD_BOT_TOKEN)
