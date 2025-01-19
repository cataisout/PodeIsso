from groq import Groq
from .vecstore import load_vecstore


def classify_question(client, question):
    router_instructions = f"""Você é um especialista em classificar perguntas.
                            Se a pergunta for sobre qualquer coisa que envolva graduação, como normas, diretrizes ou explicações de funcionamento da graduação, classifique como 'vectorstore'.
                            Para outros assuntos classifique como 'calendar_model'.
                            Retorne apenas o rótulo correspondente: 'vectorstore' ou 'calendar_model'.\n\nPergunta: {question}"""

    prompt = (
        router_instructions
    )
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=10,
        temperature=1  # Altere o valor da temperatura aqui

    )
    return response.choices[0].message.content


def retriever(vector_store, question):

  retrieved_docs = vector_store.similarity_search(question)
  return retrieved_docs


def generate_answer_with_rag(client, question, retrieved_docs):
    # Combine os documentos em um único contexto
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Crie o prompt com a pergunta e o contexto
    prompt = (
    "Você é um especialista em responder perguntas com base em documentos fornecidos. "
    "Seu objetivo é gerar uma resposta clara e precisa com base no contexto dado. Responda "
    "utilizando as informações mais relevantes do contexto. Não repita a pergunta e evite frases como 'a resposta é'. "
    "Caso a pergunta não tenha uma resposta direta, forneça informações relacionadas ou direcione para o que for mais relevante, fazendo referência aos artigos utilizados como base\n\n"
    f"Contexto:\n{context}\n\n"
    f"Pergunta: {question}\n\n"
    "Resposta:"
)

    # Envie o prompt para o modelo Groq
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=300
    )

    # Retorne a resposta gerada
    return response.choices[0].message.content.strip()


def rag(client, vecstore, question):

    docs = retriever(vecstore, question)
    answer = generate_answer_with_rag(client, question, docs)

    return answer
