import tkinter as tk
from tkinter import messagebox, ttk
import requests
import time

API_KEY_NEWS = '2c50ed24199b43b3a034f91781665591'
API_KEY_GEMINI = 'AIzaSyBrXcz_4KFf15N3FV9bRuWd4CDT7QGLIaA'

# Função para pegar o máximo de notícias
def pegar_noticias():
    url = f'https://newsapi.org/v2/everything?q=tecnologia&sortBy=publishedAt&pageSize=20&apiKey={API_KEY_NEWS}'
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados.get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar notícias: {e}")
        return None

# Função para resumir uma notícia (simples ou usando IA)
def resumir_texto_localmente(texto):
    if not texto:
        return ""
    # Fazendo um resumo básico local → depois pode trocar por uma API se quiser
    return texto[:200] + "..." if len(texto) > 200 else texto

# Função para analisar o impacto com o Gemini (resumos prontos)
def analisar_impacto_com_gemini(resumos, profissao):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = { "Content-Type": "application/json" }
    params = { "key": API_KEY_GEMINI }
    
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
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return f"Erro ao gerar análise: {str(e)}"
    except (KeyError, IndexError) as e:
        print(f"Erro ao processar resposta: {e}")
        return "Erro ao processar a análise gerada."

# Função principal
def analisar_impacto():
    profissao = entry_profissao.get()
    if not profissao:
        messagebox.showwarning("Aviso", "Por favor, insira sua profissão.")
        return

    progress_bar['value'] = 0
    progress_bar.update()
    
    try:
        noticias = pegar_noticias()
        if not noticias:
            raise Exception("Não foi possível obter notícias.")
        
        resumos = ""
        total_noticias = len(noticias)
        
        for i, noticia in enumerate(noticias):
            titulo = noticia['title']
            descricao = noticia['description'] or noticia['content']
            resumo = resumir_texto_localmente(descricao)
            resumos += f"Título: {titulo}\nResumo: {resumo}\n\n"
            
            # Atualiza progresso
            progress_bar['value'] = (i + 1) / total_noticias * 50  # 50% na parte de pegar e resumir
            progress_bar.update()
            time.sleep(0.3)  # Simula tempo
        
        # Agora chama a IA para analisar os resumos
        resultado = analisar_impacto_com_gemini(resumos, profissao)
        
        progress_bar['value'] = 100
        progress_bar.update()
        
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, resultado)
        
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        progress_bar['value'] = 0
        progress_bar.update()

# Interface
root = tk.Tk()
root.title("Impacto das Notícias na Sua Profissão")

label_profissao = tk.Label(root, text="Digite sua profissão:")
label_profissao.pack(pady=10)

entry_profissao = tk.Entry(root, width=40)
entry_profissao.pack(pady=5)

button_analizar = tk.Button(root, text="Analisar Impacto", command=analisar_impacto)
button_analizar.pack(pady=20)

progress_bar = ttk.Progressbar(root, length=300, mode='determinate', maximum=100)
progress_bar.pack(pady=10)

result_text = tk.Text(root, height=20, width=70)
result_text.pack(pady=10)

root.mainloop()
