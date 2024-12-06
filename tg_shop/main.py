from telegram import Update
import settings
from telegram.ext import(
ApplicationBuilder, CommandHandler,
MessageHandler, filters, ConversationHandler,
CallbackQueryHandler, ContextTypes
)
import db

FULL_NAME, EMAIL, RATING, FEEDBACK = 0,1,2,3

# Функція для обробки команди /start
async def start(update: Update, context):
    await update.message.reply_text("Привіт, мене цікавить ваш відгук про наш магазин! Введіть імя:) ")
    return FULL_NAME



async def name(update: Update, context):
    context.user_data['full_name'] = update.message.text
    name = update.message.text.strip().capitalize()
    if not name.isalpha():
        await update.message.reply_text("Імя повинно бути з літер!:")
        return FULL_NAME
    
    else:
        await update.message.reply_text(f"Entry your email:")
        return EMAIL


async def email(update: Update, context):
    context.user_data['email'] = update.message.text
    email = update.message.text.strip()
    if "@" in email:
        await update.message.reply_text(f"Entry rating from 1 to 5:")
        return RATING
    
    else:
        await update.message.reply_text(f"Invalid email")
        return EMAIL


async def rating(update: Update, context):
    context.user_data['rating'] = update.message.text
    rating = update.message.text.strip()
    if not int(rating) or rating > 5 or rating < 0:
        await update.message.reply_text(f"Invalid rating")
        return RATING
    else:
        await update.message.reply_text(f"Entry your feedback:")
        return FEEDBACK


async def feedback(update: Update, context):
    context.user_data['feedback'] = update.message.text
    

#Скасування реєстрації і кінець розмови
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Реєстрацію скасовано!")
    return ConversationHandler.END


# Основна частина програми
if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TOKEN).build()

    # Додаємо обробник для команди /start
    application.add_handler(CommandHandler('start', start))
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start)], #початок реєстрації (після натискання на кнопку "Зареєструватися")
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)], # перше запитання
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            RATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, rating)],
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback)],
   
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    
    # Запускаємо бота
    application.run_polling()  