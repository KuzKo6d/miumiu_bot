import os
from dotenv import load_dotenv
import db
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
#  telegram bot token
TG_TOKEN = os.getenv("TG_TOKEN")

#  ollama
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.delete(update.effective_chat.id)
    await update.message.reply_text(f'History deleted suckassfully.')


async def penis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #  fetch messages
    messages = db.read_by_chat_id(update.effective_chat.id)
    messages.append({"role": "user", "content": update.message.text})
    print(f'Context is: {messages}')

    #  response
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)

    #  catch error and answer
    if response.status_code == 200:
        print("Response:", response.json()['message']['content'])
        await update.message.reply_text(response.json()['message']['content'])
    else:
        print(f'ERROR: {response.text}')
        await update.message.reply_text(response.text)

    #  save messages
    #  save only response
    response_text = response.json()['message']['content'].split('</think>')[1][2::]
    db.write(update.message.text, update.effective_chat.id, update.effective_user.id, 'user')
    db.write(response_text, update.effective_chat.id, update.effective_user.id, 'assistant')


app = ApplicationBuilder().token(TG_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("clear", clear_history))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, penis))

app.run_polling()
