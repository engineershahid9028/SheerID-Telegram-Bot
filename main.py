
import os, logging, threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN
from db import init_db
from plans import check_plan, consume
from admin import app as admin_app

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /myplan")

async def myplan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Plan info endpoint")

async def placeholder_verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok, reason = check_plan(update.effective_user.id)
    if not ok:
        await update.message.reply_text(reason); return
    consume(update.effective_user.id)
    # PLACEHOLDER: integrate your compliant verification logic here
    await update.message.reply_text("Verification placeholder executed")

def run_admin():
    admin_app.run(host="0.0.0.0", port=8080)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myplan", myplan))
    app.add_handler(CommandHandler("verify", placeholder_verify))
    threading.Thread(target=run_admin, daemon=True).start()
    app.run_webhook(listen="0.0.0.0", port=8080, webhook_url=os.getenv("WEBHOOK_URL"))

if __name__ == "__main__":
    main()
