# -*- coding:utf-8 -*-
import os
from pathlib import Path
# Imports the Google Cloud client library
from google.cloud import language_v1

def text_nlp(text):
    # Instantiates a NLP client
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    SENTI_RESULT = client.analyze_sentiment(request={'document': document}).document_sentiment.score

    return SENTI_RESULT

if __name__ == '__main__':
    path = u'List_of_Topics_for_MS_Project_and_Thesis.txt'
    current_path = os.path.abspath('.')
    contents = Path(current_path+'/'+path).read_text()
    print(text_nlp(contents))