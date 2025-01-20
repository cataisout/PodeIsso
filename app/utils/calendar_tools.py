import transformers
from transformers import pipeline
import os

print(os.listdir())
f = open("./calendar_context.txt", "r")
context = f.read()

model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)

def calendar_response(question):
    result = nlp(question=question, context=context)
    answer= result['answer']

    return answer