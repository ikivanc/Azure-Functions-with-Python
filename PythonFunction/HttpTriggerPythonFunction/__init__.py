import logging

import azure.functions as func
from string import punctuation
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords

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
        text = ''.join([word for word in text.split() if word not in (stopwords.words('english'))])
        return func.HttpResponse(f"{text}")
    else:
        return func.HttpResponse(
             "Please pass a content on the query string or in the request body",
             status_code=400
        )