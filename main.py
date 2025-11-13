import os
import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import openai

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Load tokens from Heroku Config Vars
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

async def chatgpt_reply(update, context):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("⚠️ Error generating reply.")
        logging.error(e)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_reply))
    app.run_polling()

if __name__ == "__main__":
    main()
