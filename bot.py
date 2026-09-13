import os
import base64
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "توضیحت برای تصویر رو بفرست.\n\n"
        "مثال: یک مدل بزرگسال با استایل فشن و لباس زیر، "
        "عکس تبلیغاتی استودیویی و غیرصریح."
    )


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()

    await update.message.reply_text("⏳ در حال ساخت تصویر...")

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_bytes = base64.b64decode(result.data[0].b64_json)

        await update.message.reply_photo(
            photo=BytesIO(image_bytes),
            caption="✅ تصویر آماده شد."
        )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "❌ مشکلی در ساخت تصویر پیش آمد."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
