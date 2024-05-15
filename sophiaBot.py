import telebot
from openai import OpenAI
from dotenv import dotenv_values

# Model details
MODEL_GPT='gpt-3.5-turbo'
INSTRUCTIONS_SOPHIA="""Sophia é uma assistente virtual desenhada especificamente para empreendedores, oferecendo conselhos claros, concisos e adaptados às necessidades do seu negócio.
Sua experiência abrange uma ampla gama de tópicos relevantes para iniciar e administrar um negócio."""
INTRODUCTION_SOPHIA="Olá! Eu sou a Sophia, uma assistente virtual projetada para ajudar empreendedores com conselhos e informações relevantes para seus negócios. Como posso te ajudar hoje?"

# Initialize client gpt and telegram bot
config = dotenv_values(".env")
bot = telebot.TeleBot(config['TELEGRAM_API_KEY'])
client = OpenAI(api_key=config['OPENAI_API_KEY'])

# GPT request
def gpt_call(message_input: str):
    gpt_response = client.chat.completions.create(
        model = MODEL_GPT,
        messages = [
            {"role": "system", "content": INSTRUCTIONS_SOPHIA},
            {"role": "user", "content": message_input}
        ]
    )
    return gpt_response.choices[0].message.content

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
    response = gpt_call(msg.text)
    print(f"User: {msg.text}\nSophia: {response}")
    bot.send_message(msg.chat.id, response)

bot.polling()