# Airplane Wifi Reddit Browser Bot (Telegram)

This Telegram bot allows you to fetch text-only posts from Reddit's popular page even when on limited Wifi that only allows you to use it for. You can use it to get the latest text posts. To set up your own bot using this script, follow the directions under Getting Started.

## Table of Contents

- [No Install Use](#no-install-use)
- [Prerequisites](#prerequisites)
- [Getting Started-Self](#getting-started-self)
- [Commands](#commands)
- [Contributing](#contributing)

## No Install Use

**This is most likely what you want to use.** You may go on the Telegram app and send the message /start to @Airplane_WiFi_Reddit_bot. But if this is down and you want to try for yourself, follow instructions below.

## Prerequisites

Before you can use this bot, you need to have the following:

- Python 3.x installed on your machine.
- A Telegram bot token. You can create one by talking to the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
- Reddit API credentials (client ID, client secret, and user agent). You can obtain these by registering your bot as an application on Reddit.

## Getting Started-Self

1. Clone this repository or download the code to your local machine.

2. Navigate to directory and install the required Python packages using pip:

   ```shell
   pip install -r requirements.txt

3. Update your [Telegram bot](https://core.telegram.org/bots/features#creating-a-new-bot) and [Reddit](https://www.reddit.com/prefs/apps) tokens.
4. Run the script (has to be online) and go on your trip! We recommend using a free-tier cloud service.

## Commands
Commands you can use with the bot:

- /start: Activate the bot and start fetching posts.

- /next: Fetch the next set of text-only posts from Reddit's popular page.

- /help: Get information about the bot commands.

## Contributing
Contributions to this project are welcome! If you have any improvements or bug fixes to suggest, please feel free to open an issue (preferred) or submit a pull request.

Here is a list of things that I personally wish to implement:
- Browse comments in a similar manner (specify which post to view comments of or go down one by one for posts)
- View upvotes
- r/askreddit and similar subreddits to be formatted for easy viewing
