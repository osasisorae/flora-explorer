import telebot
from decouple import config
from messages import Messages
from engine import Educator

# Initialze Messages
messages = Messages()

# Initialie Educatro
educator = Educator()

# Initialize Telegram Bot
BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.text.startswith('/chat'):
        chat(message)
    bot.send_message(chat_id=message.chat.id, text=messages.start_message)

def chat(message):
    
    response = educator.query_vector(message.text)
    sent_msg = bot.send_message(chat_id=message.chat.id, text=response, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, chat)