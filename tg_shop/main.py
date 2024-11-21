from telegram import Update
import settings
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import db

# Функція для обробки команди /start
async def start(update: Update, context):
    await update.message.reply_text("Привіт, мене цікавить ваш відгук про наш магазин! Напишіть щось:) ")

async def echo(update: Update, context):
    await update.message.reply_text(f"Ви написали: {update.message.text}")
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# async def start(update: Update, context):
#     await update.message.reply_text("Купи слона")

# async def hi(update: Update, context):
#     await update.message.reply_text("Ні")

# async def echo(update: Update, context):
#     await update.message.reply_text(f"Усі так кажуть: {update.message.text}. А ти купи слона!")


# Основна частина програми
if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TOKEN).build()

    # Додаємо обробник для команди /start
    application.add_handler(CommandHandler('start', start))

    # Запускаємо бота
    application.run_polling()  