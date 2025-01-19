from utils.data_processing import *
from utils.custom_spliter import RegulationTextSplitter
from utils.vecstore import *


#para esse script rodar é necessário que a variável de ambiente PINECONE_API_KEY esteja corretamente configurada
pinecone_api_key = os.environ["PINECONE_API_KEY"]


if __name__ == "__main__":
    
    document = data_loader()
    splits = split_document(document)
    vecstore = load_vecstore(pinecone_api_key, index_name="regulamento")
    document_ids = vector_store.add_documents(documents=splits)