from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents.base import Document
from .custom_spliter import RegulationTextSplitter


def data_loader(path='regulamento.pdf'): 
    
    #carrega dados
    #formata corretamente


    #carregando documento
    loader = PyPDFLoader(path) 
    data = loader.load()

    #formatando 
    for doc in data:
        doc.page_content = doc.page_content.replace("\n", "")

    #jutando os documentos em um único documento
    merged_content = " ".join([doc.page_content for doc in data])
    full_document = Document(page_content=merged_content)

    return full_document


def split_document(full_document, chunk_size=1000):
    splitter = RegulationTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    chunks = splitter.split_text(full_document.page_content)

    # Converte os textos em objetos Document
    documents = [Document(page_content=text) for text in chunks]
    
    return documents



