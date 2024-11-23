from telegram import Update
import settings
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler,CallbackQueryHandler
import db

FULL_NAME, EMAIL, RATING, FEEDBACK = 0,1,2,3

# Функція для обробки команди /start
async def start(update: Update, context):
    await update.message.reply_text("Привіт, мене цікавить ваш відгук про наш магазин! Введіть імя:) ")
    return FULL_NAME



async def name(update: Update, context):
    context.user_data['full_name'] = update.message.text
    await update.message.reply_text(f"Entry your email:")

    return EMAIL


async def email(update: Update, context):
    context.user_data['email'] = update.message.text
    await update.message.reply_text(f"Entry rating from 1 to 5:")

    return RATING





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
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler( start)], #початок реєстрації (після натискання на кнопку "Зареєструватися")
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)], # перше запитання
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            RATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, rating)],
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND,city )],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    
    # Запускаємо бота
    application.run_polling()  