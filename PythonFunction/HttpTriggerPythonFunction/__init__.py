import logging

import azure.functions as func
from string import punctuation
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import pandas as pd
# We need stopwords library to remove stop words from the text
nltk.download("stopwords")
# We need the punkt library to tokenize the text
nltk.download("punkt")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    content = req.params.get('content')
    if not content:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            content = req_body.get('content')
    if content:
        # remove numeric digits
        text = ''.join(c for c in content if not c.isdigit())
        # remove punctuation and make lower case
        text = ''.join(c for c in text if c not in punctuation).lower()
        # remove stopwords from the text
        text = ' '.join([word for word in text.split() if word not in (stopwords.words('english'))])
        # remove custom stopword from a list
        customstopwords = ['marie','curie','curies','pierre',"irène", "irene",'new','time','also','one','name' ,"work", "rosalind","franklin", "first","must","never"]
        text = '–'.join(c for c in text.split(' ') if c not in customstopwords)
        text = text.replace('–', ' ')
        # tokenize the words and extract most frequent words
        allWords = nltk.tokenize.word_tokenize(text)
        fdist = FreqDist(allWords)
        topWords = [word[0] for word in fdist.most_common(30)]
        #return the result
        return func.HttpResponse(f"{topWords}")
    else:
        return func.HttpResponse(
             "Please pass a content on the query string or in the request body",
             status_code=400
        )