from typing import Optional
import requests
import logging

from lunch_menu_bot.integrations.slack.markdown import markdown_to_slack

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SlackWebhook:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def post_message(
        self, message: str, img_url: Optional[str] = None, img_small: bool = False
    ) -> bool:
        try:
            logger.info(f"Sending message: {message} and img_url: {img_url}")

            # Convert markdown to Slack-compatible format
            message = markdown_to_slack(message)
            logger.info(f"Converted message: {message}")

            # Construct the payload
            payload = {
                "blocks": [
                    {"type": "section", "text": {"type": "mrkdwn", "text": message}}
                ]
            }
            if img_url:
                img_block = {
                    "type": "image",
                    "image_url": img_url,
                    "alt_text": "Image",
                }
                if img_small:
                    payload["blocks"][0]["accessory"] = img_block
                else:
                    payload["blocks"].append(img_block)

            # Send the message
            logger.info(f"Sending payload: {payload}")
            response = requests.post(
                self.webhook_url,
                json=payload,
            )
            response.raise_for_status()
            logger.info("Message posted successfully to Slack")
            return True
        except Exception as e:
            logger.error(f"Failed to post message to Slack: {e}")
            return False
