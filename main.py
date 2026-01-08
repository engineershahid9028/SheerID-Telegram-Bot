import logging
import subprocess
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

USER_STATE = {}

TOOLS = {
    "spotify": "SheerID-Verification-Tool/spotify-verify-tool/main.py",
    "youtube": "SheerID-Verification-Tool/youtube-verify-tool/main.py",
    "google": "SheerID-Verification-Tool/one-verify-tool/main.py",
    "veterans": "SheerID-Verification-Tool/veterans-verify-tool/main.py",
    "k12": "SheerID-Verification-Tool/k12-verify-tool/main.py",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *SheerID Verification Bot*\n\n"
        "Select a service:\n"
        "/spotify\n"
        "/youtube\n"
        "/google\n"
        "/veterans\n"
        "/k12",
        parse_mode="Markdown"
    )


async def set_service(update: Update, service: str):
    USER_STATE[update.effective_user.id] = service
    await update.message.reply_text(
        f"✅ *{service.upper()} selected*\n\n"
        "Now send the SheerID verification URL.",
        parse_mode="Markdown"
    )


async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_service(update, "spotify")


async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_service(update, "youtube")


async def google(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_service(update, "google")


async def veterans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_service(update, "veterans")


async def k12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_service(update, "k12")


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    url = update.message.text.strip()

    if user_id not in USER_STATE:
        await update.message.reply_text("❌ Please select a service first.")
        return

    service = USER_STATE[user_id]
    tool_path = TOOLS.get(service)

    await update.message.reply_text("⏳ Running verification...")

    try:
        result = subprocess.run(
            ["python", tool_path, url],
            capture_output=True,
            text=True,
            timeout=180
        )

        output = result.stdout or result.stderr or "No output"

        if len(output) > 3500:
            output = output[:3500] + "\n...output truncated"

        await update.message.reply_text(
            f"📄 *Result*\n```{output}```",
            parse_mode="Markdown"
        )

    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏱ Process timed out.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spotify", spotify))
    app.add_handler(CommandHandler("youtube", youtube))
    app.add_handler(CommandHandler("google", google))
    app.add_handler(CommandHandler("veterans", veterans))
    app.add_handler(CommandHandler("k12", k12))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))

    logging.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
