import logging
from telegram.ext import Updater, MessageHandler, Filters
import openai
import os

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def chatgpt_reply(update, context):
    user_text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        reply = response["choices"][0]["message"]["content"]
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("⚠️ Error: Unable to generate reply.")
        print(e)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chatgpt_reply))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
