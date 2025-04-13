
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Logging for debugging
logging.basicConfig(level=logging.INFO)

# OpenAI API Key (Replace with your own key)
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Telegram Channel username
CHANNEL_USERNAME = '@https://t.me/allhamdulahinshallah'

# Dictionary to store message counts
user_message_counts = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('স্বাগতম! আপনি এখন GPT-র সাথে কথা বলতে পারেন।')

def check_membership(user_id, bot):
    try:
        member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def respond(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    bot = context.bot

    if user_id not in user_message_counts:
        user_message_counts[user_id] = 0
    user_message_counts[user_id] += 1

    if user_message_counts[user_id] > 50:
        if not check_membership(user_id, bot):
            update.message.reply_text(
                "🍁🍁 ইসলামিক চ্যানেল 🍁🍁\n\n"
                "পরবর্তী রিপ্লাই পেতে নিচের চ্যানেলে জয়েন করুন:\n"
                f"{CHANNEL_USERNAME}"
            )
            return

    user_message = update.message.text

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response.choices[0].text.strip()
        update.message.reply_text(bot_reply)
    except Exception as e:
        update.message.reply_text("দুঃখিত, কিছু ভুল হয়েছে।")

def main():
    # Replace with your actual Telegram Bot Token
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
