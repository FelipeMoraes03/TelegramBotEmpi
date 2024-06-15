import telebot
from openai import OpenAI
import google.generativeai as genai
from dotenv import dotenv_values

from models.connection_options.connection import dbConnectionHaddler
from models.repository.empiCollection_repository import empiCollectionRepository

db_haddle = dbConnectionHaddler()
db_haddle.connect_db()
db_connection = db_haddle.get_db_connection()
empi_collection = empiCollectionRepository(db_connection)

# Choose your model between 'GPT' and 'GEMINI'
MODEL='GEMINI'

# Model details
MODEL_GPT='gpt-3.5-turbo'
MODEL_GEMINI='gemini-1.0-pro-latest'
INSTRUCTIONS_SOPHIA="""Você é a Sophia é uma assistente virtual desenhada especificamente para empreendedores, oferecendo conselhos claros, concisos e adaptados às necessidades do seu negócio.
Sua experiência abrange uma ampla gama de tópicos relevantes para iniciar e administrar um negócio."""
INTRODUCTION_SOPHIA="Olá! Eu sou a Sophia, uma assistente virtual projetada para ajudar empreendedores com conselhos e informações relevantes para seus negócios. Como posso te ajudar hoje?"

# Initialize client gpt and telegram bot
config = dotenv_values(".env")
bot = telebot.TeleBot(config['TELEGRAM_API_KEY'])
gpt_client = OpenAI(api_key=config['OPENAI_API_KEY'])
genai.configure(api_key=config['GOOGLE_API_KEY'])

# GPT request
def gpt_call(msg: str):
    print("CALL TO GPT")
    gpt_response = gpt_client.chat.completions.create(
        model = MODEL_GPT,
        messages = [
            {"role": "system", "content": INSTRUCTIONS_SOPHIA},
            {"role": "user", "content": msg}
        ]
    )
    return gpt_response.choices[0].message.content

# Gemini request
def gemini_call(msg: str):
    print("CALL TO GEMINI")
    msg = f"{INSTRUCTIONS_SOPHIA}\n\n{msg}"
    response = genai.GenerativeModel('gemini-pro').generate_content(msg)
    return response.text

# Introduce Sophie at start
@bot.message_handler(commands=["start"])
def introduceSophia(msg):
    print(f"Sophia: {INTRODUCTION_SOPHIA}")
    bot.send_message(msg.chat.id, INTRODUCTION_SOPHIA)

def verify(msg):
    return True

# Receives user message and return GPT response
@bot.message_handler(func=verify)
def messageBot(msg):
    response = gpt_call(msg.text) if MODEL == 'GPT' else gemini_call(msg.text)
    bot.send_message(msg.chat.id, response)
    print(f"User: {msg.text}\nSophia: {response}")
    
    empi_collection.insert_document(
        {
            'request': msg.text,
            'response': response
        }
    )

bot.polling()