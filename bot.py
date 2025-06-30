from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes 
import os
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello, {update.effective_user.first_name}! I'm your bot.")

def makeRequest(prompt):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.getenv('API_KEY'))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )

    return response

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orginal_msg = update.message.reply_to_message

    if not orginal_msg or not orginal_msg.text:
        await update.message.reply_text("Please reply to a message containing text to translate.")
        return

    #translation logic
    txt_content = orginal_msg.text 
    prompt = f"Translate {txt_content} to {context.args[0] if len(context.args) != 0 else 'English'}. Ignore any links & respond with only the translation. Do not include any additional text or explanations."
 
    response = makeRequest(prompt)   
    if response and response.text: 
        await update.message.reply_text(response.text)
    else:                                                   
        await update.message.reply_text("Translation failed. Please try again later.")      
    return

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_msg = update.message.reply_to_message

    if not original_msg or not original_msg.text:
        await update.message.reply_text("Please reply to a message containing text to summarize.")
        return

    # Summarization logic
    txt_content = original_msg.text 
    prompt = f"Summarize the following text: {txt_content}. Ignore any links & respond with only the summary. Do not include any additional text or explanations."

    response = makeRequest(prompt) 
    
    if response and response.text: 
        await update.message.reply_text(response.text)
    else:
        await update.message.reply_text("Summarization failed. Please try again later.")      
    return        

# Initialize the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv('TG_KEY')).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", translate))
    app.add_handler(CommandHandler("summarize", summarize))
    print("Bot is running...")
    app.run_polling()
