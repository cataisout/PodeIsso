import os
import streamlit as st
from utils.rag_tools import classify_question, rag
from utils.vecstore import load_vecstore
from utils.calendar_tools import calendar_response
from groq import Groq

# Configurações de API
groq_api_key = os.environ["GROQ_API_KEY"]
pinecone_api_key = os.environ["PINECONE_API_KEY"]

# Inicialização
client = Groq(api_key=groq_api_key)
vecstore = load_vecstore(pinecone_api_key=pinecone_api_key)

st.title("PodeIsso?! 📚")

# Inicializar o histórico de mensagens com uma mensagem de boas-vindas
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Oi! 👋 Sou seu assistente virtual e tô aqui pra te ajudar com qualquer dúvida sobre o regulamento "
                "ou o calendário da faculdade. Quer saber sobre prazos, disciplinas ou algo assim? É só perguntar!"
            ),
        }
    ]

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if user_input := st.chat_input("Faça sua pergunta sobre regulamentos ou prazos acadêmicos..."):
    # Adicionar a pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gerar resposta
    with st.chat_message("assistant"):
        try:
            # Classificar a pergunta
            question_label = classify_question(client, user_input)

            # Responder de acordo com a classificação
            if question_label == "vectorstore":
                response = rag(client, vecstore, user_input)
            else:
                response = calendar_response(user_input)

            # Adicionar resposta ao histórico e exibir
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_message = "Desculpe, ocorreu um erro ao processar sua solicitação. 😓"
            st.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
