from langchain_pinecone import PineconeEmbeddings
import os
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone


def load_vecstore(pinecone_api_key, index_name="regulamento"):

    model_name = 'multilingual-e5-large'
    embeddings = PineconeEmbeddings(
    model=model_name,
    pinecone_api_key=pinecone_api_key
    )
    
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(index_name)

    vector_store = PineconeVectorStore(embedding=embeddings, index=index)

    return vector_store

