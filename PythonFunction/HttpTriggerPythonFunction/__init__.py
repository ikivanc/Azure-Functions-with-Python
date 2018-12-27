import logging

import azure.functions as func
from string import punctuation
import nltk
nltk.download("punkt")
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.probability import FreqDist

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
        text = text.replace('–', ' ')
        
        # remove stopwords from the text
        text = ' '.join([word for word in text.split() if word not in (stopwords.words('english'))])

        # remove custom stopword from a list
        with open("customstopwords.txt", "r") as f:
            customstopwords = f.read().splitlines()
        text = ' '.join(c for c in text.split(' ') if c not in customstopwords)
        
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