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
        "🚘 KITT iniciado.\n\n"
        "Comandos disponibles:\n"
        "/start\n"
        "/ping\n"
        "/bitcoin"
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚘 KITT está en línea"
    )


async def bitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            price = data["bitcoin"]["usd"]
        await update.message.reply_text(f"₿ Bitcoin: ${price:,} USD")
    except httpx.TimeoutException:
        await update.message.reply_text(
            "⚠️ La API de CoinGecko no respondió a tiempo. Intenta de nuevo."
        )
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        await update.message.reply_text(
            f"⚠️ Error al consultar el precio de Bitcoin: {e}"
        )
    except (KeyError, ValueError):
        await update.message.reply_text(
            "⚠️ Respuesta inesperada de la API de CoinGecko."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "⚠️ Ocurrió un error inesperado. Intenta de nuevo."
        )


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
    app.add_error_handler(error_handler)

    print("🚘 KITT iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()