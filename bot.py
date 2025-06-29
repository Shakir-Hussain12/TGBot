from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes 
import os
  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello, {update.effective_user.first_name}! I'm your bot.")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orginal_msg = update.message.reply_to_message

    if not orginal_msg or not orginal_msg.text:
        await update.message.reply_text("Please reply to a message containing text to translate.")
        return

    #translation logic
    txt_content = orginal_msg.text 
    prompt = f"Translate {txt_content} to {context.args[0] if len(context.args) != 0 else 'English'}. Ignore any links & respond with only the translation. Do not include any additional text or explanations."
    print(f"Prompt: {prompt}")

 
    from google import genai
    from google.genai import types

    load_dotenv()
    client = genai.Client(api_key=os.getenv('API_KEY'))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    ) 
    
    if response and response.text: 
        await update.message.reply_text(response.text)
    else:
        await update.message.reply_text("Translation failed. Please try again later.")      
    return
         

# Initialize the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token("8134701987:AAFu4fzaHgHKCS5vLPUO8vY7OJEibpmE7Og").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", translate))

    print("Bot is running...")
    app.run_polling()

