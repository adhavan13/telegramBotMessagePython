import os
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMNI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)



async def get_code_solution(query):
    prompt = f"""
                You are an AI code assistant. Given a programming question, respond *only* with a clean and efficient solution in the requested programming language.
                Do not provide any explanation, comments, or extra text. The response should be in a proper code block format.

                ### Example 1:
                Q: Check if a given string is a palindrome or not in Python.
                A:
                python
                def is_palindrome(s):
                    s = s.lower()
                    return s == s[::-1]

                s = input("Enter a string: ").strip()

                if is_palindrome(s):
                    print(s, 'is a palindrome.')
                else:
                    print(s, 'is not a palindrome.')
                Q: Check if a given string is a palindrome or not in Python.
                A:
                python
                def evenOrodd(s):
                    return 'even' if s % 2 == 0 else 'odd'

                s = int(input("Enter a number: "))

                print(s, is ,evenOrodd(s))
                
                now you answer the question

                Q: {query}
                A:
                """

    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Get AI-generated response
    response = model.generate_content(prompt)

    return response.text if response.text else "Error: No response from AI"

# Example Usage

async def start(update: Update, context: CallbackContext):
    """Handles the /start command."""
    await update.message.reply_text("Hello! Send me a coding question, and I'll try to answer it.")

async def handle_message(update: Update, context: CallbackContext):
    """Handles incoming messages."""
    question = update.message.text
    print(question)
    answer = await get_code_solution(question)

    await update.message.reply_text(answer)

def main():
    # Initialize the bot with the new Application class
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

