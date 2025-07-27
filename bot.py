import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = '7147755776:AAEfTB1gAmQVeUvlFlq7bwZVgq8nvdLDGAw'
BACKEND_URL = 'http://localhost:5000/predict'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /predict, чтобы получить прогноз.")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(BACKEND_URL)
    if response.status_code != 200:
        await update.message.reply_text("Ошибка получения данных.")
        return

    data = response.json()
    analysis_text = data["analysis_text"]
    predicted_price = data["predicted_price"]

    await update.message.reply_text(f"📈 Вот прогноз:\n\n{analysis_text}")
    await update.message.reply_text(f"💰 Предсказанная цена завтра: ${predicted_price:.2f}")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("predict", predict))
    application.run_polling()

if __name__ == "__main__":
    main()