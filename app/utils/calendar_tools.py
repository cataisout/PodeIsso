import transformers
from transformers import pipeline
import os

#f = open("/app/utils/calendar_context.txt", "r")
#context = f.read()

model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)

def calendar_response(question):
    #result = nlp(question=question, context=context)
    #answer= result['answer']
    answer = str(os.listdir('app/'))

    return answer