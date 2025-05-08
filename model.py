import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY_NEWS = os.getenv('API_KEY_NEWS')
API_KEY_GEMINI = os.getenv('API_KEY_GEMINI')

class NewsModel:
    def __init__(self):
        self.api_key_news = API_KEY_NEWS
        self.api_key_gemini = API_KEY_GEMINI

    def pegar_noticias(self):
        url = f'https://newsapi.org/v2/everything?q=tecnologia&sortBy=publishedAt&pageSize=20&apiKey={self.api_key_news}'
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            dados = resposta.json()
            return dados.get('articles', [])
        except Exception as e:
            print(f"Erro ao buscar notícias: {e}")
            return []

    def resumir_texto_localmente(self, texto):
        if not texto:
            return ""
        return texto[:200] + "..." if len(texto) > 200 else texto

    def analisar_impacto_com_gemini(self, resumos, profissao):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = { "Content-Type": "application/json" }
        params = { "key": self.api_key_gemini }
        
        prompt = f"Esses são os resumos das últimas notícias:\n\n{resumos}\n\nComo essas notícias podem impactar a profissão de {profissao}? Faça uma análise completa."
        
        dados = {
            "contents": [{
                "parts": [{ "text": prompt }]
            }]
        }
        
        try:
            resposta = requests.post(url, headers=headers, params=params, json=dados, timeout=60)
            resposta.raise_for_status()
            resposta_json = resposta.json()
            if 'candidates' in resposta_json and resposta_json['candidates']:
                return resposta_json['candidates'][0]['content']['parts'][0]['text']
            return "Não foi possível gerar a análise de impacto."
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return f"Erro ao gerar análise: {str(e)}"
