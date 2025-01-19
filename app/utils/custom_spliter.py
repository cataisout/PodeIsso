import re
from langchain.text_splitter import TextSplitter


class RegulationTextSplitter(TextSplitter):
    def __init__(self, chunk_size=1000, chunk_overlap=0):
        super().__init__(chunk_size, chunk_overlap)
        self.chunk_size = chunk_size

    def split_text(self, text):
        # Regex ajustada para identificar artigos nos formatos "Art. 9º" e "Art. 10."
        article_pattern = re.compile(r"(Art\. \d+[ºo]?.*?)(?=Art\. \d+[ºo]?|$)", re.DOTALL)

        # Encontra todos os artigos e seus textos completos
        articles = article_pattern.findall(text)

        # Agrupar artigos em chunks respeitando o chunk_size
        chunks = []
        current_chunk = []
        current_size = 0

        for article in articles:
            article_size = len(article)
            # Extrair o título do artigo (primeira linha)
            article_title_match = re.match(r"(Art\. \d+[ºo]?)", article)
            article_title = article_title_match.group(1) if article_title_match else ""

            # Caso o artigo inteiro seja maior que o chunk_size
            if article_size > self.chunk_size:
                # Dividir o artigo em pedaços menores
                split_article = [article[i:i + self.chunk_size] for i in range(0, article_size, self.chunk_size)]

                # Marcar os pedaços subsequentes com o título do artigo
                split_article = [
                    (chunk if idx == 0 else f"{article_title} - Continuation: {chunk}")
                    for idx, chunk in enumerate(split_article)
                ]

                # Adicionar pedaços menores ao chunk atual ou diretamente aos chunks
                if current_chunk:  # Salvar o chunk atual se existir
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_size = 0
                chunks.extend(split_article)  # Adicionar pedaços do artigo diretamente
                continue

            # Se adicionar o artigo atual excede o chunk_size, finalizar o chunk atual
            if current_size + article_size > self.chunk_size:
                if current_chunk:  # Se houver artigos acumulados, criar o chunk
                    chunks.append(" ".join(current_chunk))
                # Reiniciar para o próximo chunk
                current_chunk = [article]
                current_size = article_size
            else:
                # Adicionar artigo ao chunk atual
                current_chunk.append(article)
                current_size += article_size

        # Adicionar o último chunk, se houver
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
