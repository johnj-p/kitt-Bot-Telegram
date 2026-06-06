import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError(
        "No se encontró TELEGRAM_BOT_TOKEN en el archivo .env"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏎️ KITT Radar iniciado.\n\n"
        "Comandos disponibles:\n"
        "/start\n"
        "/ping"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏎️ KITT Radar online"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    print("🏎️ KITT Radar iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()