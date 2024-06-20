from api.config_bot import *
from api.controllers.bot_handdler import *

from models.connection_options.connection import dbConnectionHaddler
from models.repository.empiCollection_repository import empiCollectionRepository

db_haddle = dbConnectionHaddler()
db_haddle.connect_db()
db_connection = db_haddle.get_db_connection()
empi_collection = empiCollectionRepository(db_connection)

user_data = {}

# Introduce Sophie at start
@bot.message_handler(commands=["start"])
def introduce_sophia_call(msg: str) -> None:
    introduce_sophia(msg)
    bot.register_next_step_handler(msg, process_name)

# Get the type of company
def process_name(msg: str):
    # Salvando o nome
    user_id = msg.from_user.id
    user_data[user_id] = {'name': msg.text}

    # Perguntando sobre o ramo da empresa
    msg = bot.send_message(msg.chat.id, f"Olá {msg.text} é um prazer conhecê-lo. Agora, poderia me informa qual é o ramo da sua empresa?")
    bot.register_next_step_handler(msg, process_company)

def process_company(msg: str):
    user_id = msg.from_user.id
    user_data[user_id]['company'] = msg.text

    msg = bot.send_message(msg.chat.id, f"{user_data[user_id]['name']} agora você pode me informar quantos funcionários sua empresa possui?")
    bot.register_next_step_handler(msg, process_employers)

def process_employers(msg: str):
    user_id = msg.from_user.id
    user_data[user_id]['employee'] = msg.text
    msg = bot.send_message(msg.chat.id, f"Ótimo! agora consigo lhe auxiliar com respostas mais atreladas a sua realidade, em que posso lhe ajudar?")

    bot.register_next_step_handler(msg, message_bot_call)

# Final Review of Sofia
@bot.message_handler(commands=["end"])
def introduce_sophia_call(msg: str) -> None:
    bot.send_message(msg.chat.id, "Espero ter lhe ajudado a tirar todas as suas dúvidas, como você classifica a sua experiência em uma nota de 0 a 5")
    bot.register_next_step_handler(msg, process_employers)

# Get the user rate
def process_rate(msg: str) -> None:
    user_id = msg.from_user.id
    user_data[user_id]['rating'] = msg.text

    bot.send_message(msg.chat.id, "Caso queira deixar algum feedback escrito, sinta-se a vontade para escrever. Foi um prazer conversar com você! \n\ncaso deseje recomeçar a conversa digite /start")
    bot.register_next_step_handler(msg, process_feedback)

# Get user feedback
def process_feedback(msg: str) -> None:
    user_id = msg.from_user.id
    user_data[user_id]['feedback'] = msg.text

    bot.send_message(msg.chat.id, f"Obrigado pelo FeedBack {user_data[user_id]['name']}!")

# Receives user message and return GPT response
@bot.message_handler(func=(lambda x: True))
def message_bot_call(msg: str) -> None:
    empi_collection.insert_document(
        message_bot(msg, user_data)
    )

bot.polling()