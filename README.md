# Lunch Menu Bot

A Discord bot that fetches the daily lunch menu and formats it beautifully.

## Features

- Fetches daily lunch menu from a specified source.
- Formats the menu and makes it ✨pretty✨.
- Adds english translations using OpenAI.
- Posts the formatted menu

## Requirements

- Python 3.12
- [OpenAI API Key](https://beta.openai.com/signup/)
- Either
  - [Discord API Token](https://discord.com/developers/applications)
  - [Slack webhook URL](https://api.slack.com/messaging/webhooks)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/aseligmann/lunch-menu-bot.git
    cd lunch-menu-bot
    ```

2. Set up environment variables:
    Create a `.secrets` file in the root directory and add your tokens:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    DISCORD_BOT_TOKEN=your_discord_bot_token
    SLACK_WEBHOOK_URL=your_slack_webhook_url
    ```

3. Run docker-compose:
    ```sh
    docker-compose up -d
    ```
