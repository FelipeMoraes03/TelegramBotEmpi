from openai import OpenAI
import google.generativeai as genai
from dotenv import dotenv_values

# Initialize gpt and gemini clients
config = dotenv_values(".env")
gpt_client = OpenAI(api_key=config['OPENAI_API_KEY'])
genai.configure(api_key=config['GOOGLE_API_KEY'])

# Model details
MODEL_GPT='gpt-3.5-turbo'
MODEL_GEMINI='gemini-1.5-pro-001'
INSTRUCTIONS_SOPHIA="""Você é a Sophia é uma assistente virtual desenhada especificamente para empreendedores, oferecendo conselhos claros, concisos e adaptados às necessidades do seu negócio.
Sua experiência abrange uma ampla gama de tópicos relevantes para iniciar e administrar um negócio."""

# GPT request
def gpt_call(msg: str) -> str:
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
def gemini_call(msg: str, user_data: dict, id: int) -> str:
    print("CALL TO GEMINI")
    msg = f"{INSTRUCTIONS_SOPHIA}\nPessoa para que você irá responder: {user_data[id]['name']}\nTipo da empresa que ele possui: {user_data[id]['company']}\n A empressa possui essa quantiadade de funcionários {user_data[id]['employee']}\n\n{msg}"
    response = genai.GenerativeModel('gemini-pro').generate_content(msg)
    return response.text