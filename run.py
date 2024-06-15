from api.config_bot import *
from api.controllers.bot_handdler import *

from models.connection_options.connection import dbConnectionHaddler
from models.repository.empiCollection_repository import empiCollectionRepository

db_haddle = dbConnectionHaddler()
db_haddle.connect_db()
db_connection = db_haddle.get_db_connection()
empi_collection = empiCollectionRepository(db_connection)

# Introduce Sophie at start
@bot.message_handler(commands=["start"])
def introduce_sophia_call(msg: str) -> None:
    introduce_sophia(msg)

# Receives user message and return GPT response
@bot.message_handler(func=(lambda x: True))
def message_bot_call(msg: str) -> None:
    empi_collection.insert_document(
        message_bot(msg)
    )

bot.polling()