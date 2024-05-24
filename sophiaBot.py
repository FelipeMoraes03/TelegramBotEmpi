import telebot
from openai import OpenAI
import google.generativeai as genai
from dotenv import dotenv_values

# Choose your model between 'GPT' and 'GEMINI'
MODEL='GEMINI'

# Model details
MODEL_GPT='gpt-3.5-turbo'
MODEL_GEMINI='gemini-1.0-pro-latest'

INSTRUCTIONS_SOPHIA="""Você é a Sophia é uma assistente virtual desenhada especificamente para empreendedores, oferecendo conselhos claros, concisos e adaptados às necessidades do seu negócio.
Sua experiência abrange uma ampla gama de tópicos relevantes para iniciar e administrar um negócio."""

END_PROMPT="""Explique o porque esse problema ocorre contextualizando com o tipo de negócio, ensine a pessoa a resolver esse problema de forma pratica, simples, com exemplos, traçando estratégias para resolver esse problema.
Certifique-se de expor métodos e passo a passo para que o empreendedor resolva o problema"""

INTRODUCTION_SOPHIA="""Olá! Eu sou a Sophia, uma assistente virtual projetada para ajudar empreendedores com conselhos e informações relevantes para seus negócios.
Selecione qual a sua área de atuação dentre as seguintes opções (Clique no item específico):

- Se seu negócio está na área de Bares e Restaurantes, selecione /Bares
- Se seu negócio está na área de Serviços de Estéticas, selecione /Estetica
- Se seu negócio está na área de Fabricantes de Roupas, selecione /Roupas
- Se seu negócio não se encontra em nenhuma área acima, selecione /Outros"""

BASE_PROMPTS={
    'Bar1': "-Ramo de atuação: Bares e Restaurantes \n -Problema: Não tomo decisão com indicadores financeiros",
    'Bar2': "-Ramo de atuação: Bares e Restaurantes \n -Problema: Tenho dificuldade de precificar meus produtos",
    'Bar3': "-Ramo de atuação: Bares e Restaurantes \n -Problema: Passo períodos sem dinheiro em caixa",
    'Estetica1': "-Ramo de atuação: Serviços de Estéticas \n -Problema: Não sei precificar meu serviço",
    'Estetica2': "-Ramo de atuação: Serviços de Estéticas \n -Problema: Tenho dificuldade com controle de contas a pagar e receber",
    'Estetica3': "-Ramo de atuação: Serviços de Estéticas \n -Problema: Dificuldade de monitorar indicadores financeiros",
    'Roupas1': "-Ramo de atuação: Fabricantes de Roupas \n -Problema: Tenho dificuldade em precificar meu produto",
    'Roupas2': "-Ramo de atuação: Fabricantes de Roupas \n -Problema: Não faço planejamento financeiro",
    'Roupas3': "-Ramo de atuação: Fabricantes de Roupas \n -Problema: Não separo finanças pessoais das da empresa",
    'Outros1': "-Problema: Não sei precificar Produtos e Serviços",
    'Outros2': "-Problema: Não consigo controlar a entrada e saída de dinheiro e quanto preciso ter em caixa",
    'Outros3': "-Problema: Não tenho ou não tomo decisão baseado em indicadores financeiros",
    'Outros4': "-Problema: Tenho dificuldade de pegar Crédito/empréstimo e/ou fazer investimentos",
    'Outros5': "-Problema: Não costumo fazer planejamento financeiro"
}

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
def introduce_sophia(msg):
    print(f"Sophia: {INTRODUCTION_SOPHIA}\n")
    bot.send_message(msg.chat.id, INTRODUCTION_SOPHIA)

def verify(msg):
    return True

@bot.message_handler(commands=['Bares'])
def sugest_bares(msg):
    response = f"""Você selecionou a opção de {msg.text[1:]}.
Aqui estão as dúvidas mais frequentes de sua área. Selecione alguma das dúvidas ou escreva sua dúvida específica no chat.
/Bar1 - Não tomo decisão com indicadores financeiros
/Bar2 - Tenho dificuldade de precificar meus produtos
/Bar3 - Passo períodos sem dinheiro em caixa
"""
    bot.send_message(msg.chat.id, response)

@bot.message_handler(commands=['Estetica'])
def sugest_bares(msg):
    response = f"""Você selecionou a opção de {msg.text[1:]}.
Aqui estão as dúvidas mais frequentes de sua área. Selecione alguma das dúvidas ou escreva sua dúvida específica no chat.
/Estetica1 - Não sei precificar meu serviço
/Estetica2 - Tenho dificuldade com controle de contas a pagar e receber
/Estetica3 - Dificuldade de monitorar indicadores financeiros
"""
    bot.send_message(msg.chat.id, response)

@bot.message_handler(commands=['Roupas'])
def sugest_bares(msg):
    response = f"""Você selecionou a opção de {msg.text[1:]}.
Aqui estão as dúvidas mais frequentes de sua área. Selecione alguma das dúvidas ou escreva sua dúvida específica no chat.
/Roupas1 - Tenho dificuldade em precificar meu produto
/Roupas2 - Não faço planejamento financeiro
/Roupas3 - Não separo finanças pessoais das da empresa
"""
    bot.send_message(msg.chat.id, response)

@bot.message_handler(commands=['Outros'])
def sugest_bares(msg):
    response = f"""Você selecionou a opção de {msg.text[1:]}.
Aqui estão as dúvidas mais frequentes de sua área. Selecione alguma das dúvidas ou escreva sua dúvida específica no chat.
/Outros1 - Não sei precificar Produtos e Serviços
/Outros2 - Não consigo controlar a entrada e saída de dinheiro e quanto preciso ter em caixa 
/Outros3 - Não tenho ou não tomo decisão baseado em indicadores financeiros
/Outros4 - Tenho dificuldade de pegar Crédito/empréstimo e/ou fazer investimentos
/Outros5 - Não costumo fazer planejamento financeiro
"""
    bot.send_message(msg.chat.id, response)

@bot.message_handler(commands=['Bar1', 'Bar2', 'Bar3', 'Estetica1', 'Estetica2', 'Estetica3','Roupas1',
                               'Roupas2', 'Roupas3', 'Outros1','Outros2','Outros3','Outros4','Outros5'])
def sugest_bares(msg):
    message = BASE_PROMPTS[msg.text[1:]] + END_PROMPT
    response = gpt_call(message) if MODEL == 'GPT' else gemini_call(message)
    bot.send_message(msg.chat.id, response)

# Receives user message and return GPT response
@bot.message_handler(func=verify)
def message_bot(msg):
    response = gpt_call(msg.text) if MODEL == 'GPT' else gemini_call(msg.text)
    print(f"User: {msg.text}\nSophia: {response}")
    bot.send_message(msg.chat.id, response)

bot.polling()