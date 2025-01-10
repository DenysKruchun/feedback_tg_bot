from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
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


    
    # await update.message.reply_text(f"{update.message.chat_id}") # отримуєммо ID чату

    return FULL_NAME



async def name(update: Update, context):
    name = update.message.text.strip().capitalize()
    if not name.isalpha():
        await update.message.reply_text("Імя повинно бути з літер!:")
        return FULL_NAME
    else:
        context.user_data['full_name'] = name
        await update.message.reply_text(f"Entry your email:")
        return EMAIL


async def email(update: Update, context):
    
    email = update.message.text.strip()
    if "@" in email:
        context.user_data['email'] = update.message.text
        keyboard = [
            [InlineKeyboardButton("1", callback_data = "1")],
            [InlineKeyboardButton("2", callback_data = "2")],
            [InlineKeyboardButton("3", callback_data = "3")],
            [InlineKeyboardButton("4", callback_data = "4")],
            [InlineKeyboardButton("5", callback_data = "5")]
        ]        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose your rating!", reply_markup=reply_markup)
        return FEEDBACK
    else:
        await update.message.reply_text(f"Invalid email")
        return EMAIL
    

        


async def rating(update: Update, context): #rating
    query = update.callback_query
    await query.answer()
    rating = query.data
    await query.edit_message_text(text = f"Selected option {rating}")
    context.user_data['rating'] = rating
    await query.message.reply_text(f"Entry your feedback:")
    return FEEDBACK 
 




async def feedback(update: Update, context):
    context.user_data['feedback'] = update.message.text
    await update.message.reply_text("THANKS FOR REGISTRATION")
    text = f''' New feedback was created: 
Ім'я: {context.user_data['full_name']}
Email:{context.user_data['email']}
Rating: {context.user_data['rating']}
Feedback: {context.user_data['feedback']}'''
    await context.bot.send_message(chat_id = settings.CHAT_ID, text = text )
    


    

#Скасування реєстрації і кінець розмови
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Реєстрацію скасовано!")
    return ConversationHandler.END


# Основна частина програми
if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TOKEN).build()
    

    # Додаємо обробник для команди /start
    application.add_handler(CallbackQueryHandler(rating))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
         #початок реєстрації (після натискання на кнопку "Зареєструватися")
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)], # перше запитання
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            # RATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, rating)],
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback)],
#    https://github.com/volodymyrlogika/tg_feedback/actions
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(rating))

    
    # Запускаємо бота
    application.run_polling()  