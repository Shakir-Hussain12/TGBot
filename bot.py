from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes 
  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello, {update.effective_user.first_name}! I'm your bot.")

         

# Initialize the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token("8134701987:AAFu4fzaHgHKCS5vLPUO8vY7OJEibpmE7Og").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", translate))

    print("Bot is running...")
    app.run_polling()

