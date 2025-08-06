from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyCLOjddr_B-6HwPCqLjsswHLYezZCvDn8E')

def get_service_ai_bio(service_name):
    prompt='''
    Me mostre uma descrição para o processo {} em no máximo 150 carecteres.
    Fale coisas específicas sobre esse serviço. Você tem a demanda de criar uma descrição simples e direta sobre o serviço mencionado.
    Você deve retornar apenas a descrição, sem formatação ou explicações adicionais, pois essas informações vão direto para a descrição do serviço mencionado.
    '''
    prompt = prompt.format(service_name)

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=30)
        )
    )
    return response.text
