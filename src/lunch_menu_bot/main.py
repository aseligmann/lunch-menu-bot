import asyncio
import logging
import random
import os
from typing import Optional
import schedule
from dotenv import dotenv_values
from lunch_menu_bot.integrations.discord.bot import LunchMenuBot
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
DISCORD_BOT_TOKEN = config["DISCORD_BOT_TOKEN"]
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
        msg = "¯\\_(ツ)_/¯ no menu available"
        return (msg, None)
    if day not in menu or menu[day] is None:
        logger.warning("No menu found for today")
        msg = "looks like the chef took a day off 🥺"
        return (msg, None)

    logger.info("Prettifying the menu...")

    menu_raw = menu[day]
    logger.info(f"Menu for {day}: {menu_raw}")

    menu_pretty = remove_empty_lines(prettify(openai_client, menu_raw))
    logger.info(f"Prettified menu for {day}: {menu_pretty}")

    embed = None
    alert_keywords = ["hønsesalat", "kyllingesalat"]
    if any(keyword in menu_raw.lower() for keyword in alert_keywords):  # hønse alert?
        # EXTREME importance fucking spread the word SEND IT !!!
        embed = random.choice(EMBED_GIFS["chicken"])

    return (menu_pretty, embed)


async def main():
    # Read integration selection from environment variables
    run_slack = os.environ.get("RUN_SLACK", "true").lower() == "true"
    run_discord = os.environ.get("RUN_DISCORD", "true").lower() == "true"

    # Log what's being run
    logger.info(f"Running with: Slack={run_slack}, Discord={run_discord}")

    try:
        tasks = []

        if run_slack:

            async def slack_webhook_scheduler():
                def slack_get_and_post_menu():
                    msg, img_url = get_menu()
                    slack_webhook.post_message(msg, img_url)

                # Schedule job for 11:30 AM UTC+1 on weekdays
                t = "11:30"
                tz = "Europe/Copenhagen"
                schedule.every().monday.at(t, tz=tz).do(slack_get_and_post_menu)
                schedule.every().tuesday.at(t, tz=tz).do(slack_get_and_post_menu)
                schedule.every().wednesday.at(t, tz=tz).do(slack_get_and_post_menu)
                schedule.every().thursday.at(t, tz=tz).do(slack_get_and_post_menu)
                schedule.every().friday.at(t, tz=tz).do(slack_get_and_post_menu)

                while True:
                    schedule.run_pending()
                    await asyncio.sleep(60.0)

            # Start the Slack webhook scheduler
            logger.info("Starting Slack lunch menu scheduler...")
            slack_webhook_task_handle = asyncio.create_task(slack_webhook_scheduler())
            tasks.append(slack_webhook_task_handle)

        if run_discord:
            # Start the Discord bot
            logger.info("Starting Discord lunch menu bot...")
            bot = LunchMenuBot(func_get_menu=get_menu)
            discord_bot_task_handle = asyncio.create_task(bot.start(DISCORD_BOT_TOKEN))
            tasks.append(discord_bot_task_handle)

        if tasks:
            # Wait for all active tasks to complete
            await asyncio.gather(*tasks)
        else:
            logger.warning("No integrations selected. Exiting...")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
    finally:
        logger.info("Exiting...")


if __name__ == "__main__":
    # message, embed = get_menu()
    # logger.info(f"Message: {message}")
    # logger.info(f"Embed: {embed}")

    asyncio.run(main())
