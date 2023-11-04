from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import praw
import logging

reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='YOUR_USER_AGENT')

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

current_index = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Welcome! This bot provides text-only posts from Reddit\'s popular page. '
        'Use /next to get the latest text posts.')

def next_posts(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in current_index:
        current_index[chat_id] = None

    count = 0
    while count < 5:
        posts = reddit.subreddit('popular').hot(limit=10, params={'after': current_index[chat_id]})
        for submission in posts:
            if not (vars(submission).get('is_video') or vars(submission).get('is_gallery') or vars(submission).get('post_hint')):
                message = f"{submission.title}\n{submission.url}"
                update.message.reply_text(message)
                count += 1
                if count >= 5:
                    break

        current_index[chat_id] = posts[-1].fullname

        if count < 5:
            continue

def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Here are the commands you can use:\n"
        "/start - Activate the bot and start fetching posts.\n"
        "/next - Fetch the next set of text-only posts from Reddit's popular page.\n"
        "/help - Get information about the bot commands.\n"
    )
    update.message.reply_text(help_text)

def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("next", next_posts))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
