import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import praw

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Reddit with the provided credentials
reddit = praw.Reddit(client_id='kSziYY2zGJP_DkJzhgHjFg',
                     client_secret='q3drKzNCS0lHUXPM9oo6dP6dXWg8Kg',
                     user_agent='brbcryinginside')

# Your Telegram Bot Token
TELEGRAM_TOKEN = '6905195665:AAFA8SaN7-BYR7l_3XvlJmZe_WDf3hnDc3c'

# Dictionary to keep track of the last post ID for pagination
last_post_id = {}

def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "You can control me by sending these commands:\n\n"
        "/start - Start interacting with the bot\n"
        "/fetchreddit - Fetch the top 5 text-only posts from Reddit's popular page\n"
        "/next - Get the next set of posts\n"
        "/help - Show this help message"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def fetch_reddit(update: Update, context: CallbackContext, next_page=False) -> None:
    chat_id = update.effective_chat.id
    after_post_id = last_post_id.get(chat_id) if next_page else None

    # Fetch posts from r/all sorted by 'hot'
    subreddit = reddit.subreddit('all')
    posts = list(subreddit.hot(limit=10, params={"after": after_post_id}))
    text_posts = [post for post in posts if not post.is_video and "image" not in post.url and "imgur" not in post.url][:5]
    
    for index, post in enumerate(text_posts, 1):
        # Send post title and URL
        context.bot.send_message(chat_id=chat_id, text=f"Post #{index}:\n{post.title}\n{post.url}")
        
        post.comment_sort = 'best'
        post.comments.replace_more(limit=0)
        comments = post.comments.list()[:5]
        
        # Format and send top comments
        comments_text = "\n".join([f"{idx}. {comment.body}" for idx, comment in enumerate(comments, 1)])
        context.bot.send_message(chat_id=chat_id, text=f"Top comments for post #{index}:\n{comments_text}")

    if text_posts:
        last_post_id[chat_id] = text_posts[-1].fullname

def next_posts(update: Update, context: CallbackContext) -> None:
    fetch_reddit(update, context, next_page=True)

def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('fetchreddit', fetch_reddit))
    dispatcher.add_handler(CommandHandler('next', next_posts))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
