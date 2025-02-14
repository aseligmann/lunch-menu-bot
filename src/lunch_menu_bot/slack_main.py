import logging
import random
from typing import Optional
import schedule
import time
from dotenv import dotenv_values
from lunch_menu_bot.integrations.slack.webhook import SlackWebhook
from lunch_menu_bot.integrations.constants import EMBED_GIFS
from lunch_menu_bot.format.openai import get_client, prettify, remove_empty_lines
from lunch_menu_bot.menu.kragerup_og_ko import fetch_menu_page, parse_menu_page
from lunch_menu_bot.time.time import get_week_and_day

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
config = dotenv_values(".secrets")
SLACK_WEBHOOK_URL = config["SLACK_WEBHOOK_URL"]
OPENAI_API_KEY = config["OPENAI_API_KEY"]

openai_client = get_client(OPENAI_API_KEY)
slack_webhook = SlackWebhook(SLACK_WEBHOOK_URL)


def get_menu() -> tuple[str, Optional[str]]:
    logger.info("Fetching the menu...")
    html_content = fetch_menu_page()

    logger.info("Parsing the menu...")
    week_number, day = get_week_and_day()
    column_identifier = f"Uge {week_number}"
    menu = parse_menu_page(html_content, column_identifier)

    # Check validity
    if menu is None:
        logger.error("No menu found")
        msg = random.choice(
            [
                "¯\\_(ツ)_/¯ ",
                "wtf no food today??",
                "maybe try wolt?",
            ]
        )
        return (msg, EMBED_GIFS["fail"])
    if day not in menu:
        logger.warning("No menu found for today")
        msg = random.choice(
            [
                "you get nothing, try again tomorrow",
                "looks like the chef took a day off",
                "check mia channel for menu",
            ]
        )
        return (msg, EMBED_GIFS["confused"])

    logger.info("Prettifying the menu...")

    menu_raw = menu[day]
    logger.info(f"Menu for {day}: {menu_raw}")

    menu_pretty = remove_empty_lines(prettify(openai_client, menu_raw))
    logger.info(f"Prettified menu for {day}: {menu_pretty}")

    embed = None
    if "hønsesalat" in menu_raw.lower():  # hønse alert?
        # EXTREME importance fucking spread the word SEND IT !!!
        embed = random.choice(
            [EMBED_GIFS["chicken1"], EMBED_GIFS["chicken2"], EMBED_GIFS["chicken3"]]
        )

    return (menu_pretty, embed)


def main():
    logger.info("Starting Slack lunch menu scheduler...")

    def get_and_post_menu():
        msg, img_url = get_menu()
        slack_webhook.post_message(msg, img_url)

    # Schedule job for 11:30 AM UTC+1 on weekdays
    t = "11:30"
    tz = "Europe/Copenhagen"
    schedule.every().monday.at(t, tz=tz).do(get_and_post_menu)
    schedule.every().tuesday.at(t, tz=tz).do(get_and_post_menu)
    schedule.every().wednesday.at(t, tz=tz).do(get_and_post_menu)
    schedule.every().thursday.at(t, tz=tz).do(get_and_post_menu)
    schedule.every().friday.at(t, tz=tz).do(get_and_post_menu)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
