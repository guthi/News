import time

class NewsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def analisar_impacto(self):
        profissao = self.view.get_profissao()
        if not profissao:
            self.view.show_warning("Por favor, insira sua profissão.")
            return
        
        self.view.update_progress(0)

        try:
            noticias = self.model.pegar_noticias()
            if not noticias:
                raise Exception("Não foi possível obter notícias.")
            
            resumos = ""
            total = len(noticias)

            for i, noticia in enumerate(noticias):
                titulo = noticia['title']
                descricao = noticia['description'] or noticia['content']
                resumo = self.model.resumir_texto_localmente(descricao)
                resumos += f"Título: {titulo}\nResumo: {resumo}\n\n"

                progresso = (i + 1) / total * 50
                self.view.update_progress(progresso)
                time.sleep(0.2)

            resultado = self.model.analisar_impacto_com_gemini(resumos, profissao)

            self.view.update_progress(100)
            self.view.show_result(resultado)

        except Exception as e:
            self.view.show_error(str(e))
            self.view.update_progress(0)
