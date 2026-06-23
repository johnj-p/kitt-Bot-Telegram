import os

import httpx
from dotenv import load_dotenv
from telegram import BotCommand, Update
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
        "🏎️ KITT iniciado.\n\n"
        "Comandos disponibles:\n"
        "/start\n"
        "/ping\n"
        "/bitcoin"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏎️ KITT está en línea"
    )


async def bitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        price = data["bitcoin"]["usd"]
    await update.message.reply_text(f"₿ Bitcoin: ${price:,} USD")


async def post_init(app: Application):
    commands = [
        BotCommand("start", "Iniciar el bot"),
        BotCommand("ping", "Verificar si el bot está en línea"),
        BotCommand("bitcoin", "Precio actual de Bitcoin"),
    ]
    await app.bot.set_my_commands(commands)


def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("bitcoin", bitcoin))

    print("🏎️ KITT iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()