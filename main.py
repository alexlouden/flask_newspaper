import json
import os
import urlparse
import nltk
from flask import Flask
from newspaper import Article

app = Flask(__name__)
app.secret_key = "aqPcSglaNdxTVKjYOV31y6boasfkmasf;lkmasflknasgi"


class SetSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return json.dumps(list(obj))

        return json.JSONEncoder.default(self, obj)


@app.route('/<path:url>')
def home(url):

    data = {}
    data['url'] = url

    # Validate url
    if urlparse.urlparse(url).scheme not in ('http', 'https'):
        data['error'] = 'Invalid URL'
        return json.dumps(data)

    a = Article(url)
    a.download()
    a.parse()

    data['title'] = a.title
    data['authors'] = a.authors
    data['text'] = a.text

    a.nlp()

    # NLP
    data['summary'] = a.summary
    data['keywords'] = a.keywords
    data['tags'] = a.tags

    # Media
    data['top_image'] = a.top_image
    data['images'] = a.images
    data['movies'] = a.movies

    # Meta
    data['source_url'] = a.source_url
    data['published_date'] = a.published_date

    data['meta_img'] = a.meta_img
    data['meta_keywords'] = a.meta_keywords
    data['meta_lang'] = a.meta_lang

    return json.dumps(data, cls=SetSerializer)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    # Check nltk has punkt tokenizer
    nltk.download('punkt')

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
