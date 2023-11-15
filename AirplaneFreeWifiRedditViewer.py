import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import praw

# Logging on serverside
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

reddit = praw.Reddit(client_id='kSziYY2zGJP_DkJzhgHjFg',
                     client_secret='q3drKzNCS0lHUXPM9oo6dP6dXWg8Kg',
                     user_agent='brbcryinginside')

TELEGRAM_TOKEN = '6905195665:AAFA8SaN7-BYR7l_3XvlJmZe_WDf3hnDc3c'

# Dictionary for pagination / last post ID 
last_post_id = {}

def send_long_message(chat_id, text, context):
    """Splits long messages and sends them separately to avoid the message length limit."""
    MAX_MESSAGE_LENGTH = 4096
    for x in range(0, len(text), MAX_MESSAGE_LENGTH):
        context.bot.send_message(chat_id=chat_id, text=text[x:x+MAX_MESSAGE_LENGTH])

def fetch_subreddit_posts(update, context, subreddit_name, next_page=False):
    chat_id = update.effective_chat.id
    after_post_id = last_post_id.get(chat_id) if next_page else None

    subreddit = reddit.subreddit(subreddit_name)
    posts = list(subreddit.hot(limit=10, params={"after": after_post_id}))
    text_posts = [post for post in posts if not post.is_video and "image" not in post.url and "imgur" not in post.url][:5]

    for index, post in enumerate(text_posts, 1):
        post_message = f"Post #{index}:\nTitle: {post.title}\nUpvotes: {post.score}\nURL: {post.url}"
        send_long_message(chat_id, post_message, context)
        
        post.comment_sort = 'best'
        post.comments.replace_more(limit=0)
        comments = post.comments.list()[:5]
        comments_text = "\n".join([f"{idx}. {comment.body} - {comment.score} upvotes" for idx, comment in enumerate(comments, 1)])
        
        if comments_text:
            send_long_message(chat_id, f"Top comments for Post #{index}:\n{comments_text}", context)
        else:
            context.bot.send_message(chat_id=chat_id, text="No comments to display.")

    if text_posts:
        last_post_id[chat_id] = text_posts[-1].fullname

def fetch_reddit(update: Update, context: CallbackContext) -> None:
    args = context.args
    subreddit_name = 'all' if not args else args[0]
    fetch_subreddit_posts(update, context, subreddit_name)


def next_posts(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    subreddit_name = last_post_id.get(chat_id, {}).get('subreddit', 'all')
    fetch_subreddit_posts(update, context, subreddit_name, next_page=True)


def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Commands:\n"
        "/start - Start interacting with the bot\n"
        "/fetchreddit [subreddit] - Fetch top posts from a specified subreddit (default is 'all')\n"
        "/next - Get the next set of posts from the same subreddit\n"
        "/help - Show this help message"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('fetchreddit', fetch_reddit, pass_args=True))
    dispatcher.add_handler(CommandHandler('next', next_posts))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
