import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import time

# Suas chaves de API
API_KEY_NEWS = '2c50ed24199b43b3a034f91781665591'
API_KEY_GEMINI = 'AIzaSyBrXcz_4KFf15N3FV9bRuWd4CDT7QGLIaA'

# Função para pegar as notícias
def pegar_noticias():
    url = f'https://newsapi.org/v2/everything?q=tesla&from=2025-04-08&sortBy=publishedAt&apiKey={API_KEY_NEWS}'
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Isso vai levantar uma exceção para códigos 4XX/5XX
        dados = resposta.json()
        return dados.get('articles', [])  # Retorna lista vazia se 'articles' não existir
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar notícias: {e}")
        return None
    except ValueError as e:  # Caso o JSON seja inválido
        print(f"Erro ao decodificar JSON: {e}")
        return None
# Função para resumir usando a API Gemini
def resumir_com_gemini(texto):
    if not texto or not isinstance(texto, str):
        return "Texto inválido para resumo"
    
    # Verifique a URL correta da API do Gemini - este é um exemplo, consulte a documentação oficial
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers = {
        "Content-Type": "application/json"
    }
    
    params = {
        "key": API_KEY_GEMINI  # A API do Gemini geralmente usa key como parâmetro, não Bearer token
    }
    
    dados = {
        "contents": [{
            "parts": [{
                "text": f"Resuma este texto de forma concisa: {texto}"
            }]
        }]
    }
    
    try:
        resposta = requests.post(
            url,
            headers=headers,
            params=params,
            json=dados,
            timeout=30
        )
        resposta.raise_for_status()
        
        resposta_json = resposta.json()
        
        # A estrutura de resposta pode variar - ajuste conforme a documentação oficial
        if 'candidates' in resposta_json and resposta_json['candidates']:
            return resposta_json['candidates'][0]['content']['parts'][0]['text']
        return "Não foi possível gerar o resumo"
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return f"Erro ao gerar resumo: {str(e)}"
    except (KeyError, IndexError) as e:
        print(f"Erro ao processar resposta: {e}")
        return "Erro ao processar o resumo gerado"

# Função para analisar o impacto na profissão
def analisar_impacto():
    profissao = entry_profissao.get()
    if not profissao:
        messagebox.showwarning("Aviso", "Por favor, insira sua profissão.")
        return

    # Ativar barra de progresso
    progress_bar['value'] = 0
    progress_bar.update()

    # Começa a análise e busca de notícias
    try:
        noticias = pegar_noticias()
        if not noticias:
            raise Exception("Erro ao buscar notícias.")

        impacto = []
        total_noticias = len(noticias)
        
        for i, noticia in enumerate(noticias[:5]):  # Pegando as 5 primeiras notícias
            titulo = noticia['title']
            descricao = noticia['description'] or noticia['content']
            if descricao:
                resumo = resumir_com_gemini(descricao)
                impacto.append(f"Notícia: {titulo}\nResumo: {resumo}\nComo pode impactar {profissao}:")
                impacto.append(f"Análise: A notícia pode afetar sua área de atuação de diversas formas, dependendo das tendências tecnológicas, riscos ou mudanças no mercado.")
            
            # Atualizando barra de progresso
            progress_bar['value'] = (i + 1) / 5 * 100
            progress_bar.update()
            time.sleep(1)  # Simulando um pequeno atraso para visualizar a barra de progresso

        # Exibindo o impacto na interface
        result_text.delete(1.0, tk.END)  # Limpa o campo de resultado
        for item in impacto:
            result_text.insert(tk.END, item + "\n\n")

    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        # Barra de progresso chega ao final
        progress_bar['value'] = 100
        progress_bar.update()

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Impacto das Notícias na Sua Profissão")

# Label e Entry para profissão
label_profissao = tk.Label(root, text="Digite sua profissão:")
label_profissao.pack(pady=10)

entry_profissao = tk.Entry(root, width=40)
entry_profissao.pack(pady=5)

# Botão para analisar impacto
button_analizar = tk.Button(root, text="Analisar Impacto", command=analisar_impacto)
button_analizar.pack(pady=20)

# Barra de progresso
progress_bar = ttk.Progressbar(root, length=300, mode='determinate', maximum=100)
progress_bar.pack(pady=10)

# Área de texto para mostrar o resultado
result_text = tk.Text(root, height=15, width=60)
result_text.pack(pady=10)

# Iniciando o loop do Tkinter
root.mainloop()
