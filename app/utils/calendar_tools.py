import transformers
from transformers import pipeline
import os

f = open("app/utils/calendar_context.txt", "r")
context = f.read()

model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)

def get_answer_line(context, start_position):
    lines = context.split('\n')
    count = 0

    for line in lines:
        if count + len(line) + 1 > start_position:
            text = ','.join(line.split(',')[:-1]) + '.'
            return text
        
        count += len(line) + 1

def calendar_response(question):
    result = nlp(question=question, context=context)
    answer= f"{result['answer']} -> {get_answer_line(context, result['start'])}"

    return answer