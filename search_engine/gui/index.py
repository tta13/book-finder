import os
from flask import Flask, render_template, request, url_for, redirect
from utils import *

app = Flask(__name__)

results = {
    "field_results": [
        {
            'title': 'Manifesto comunista',
            'publisher': 'Boitempo',
            'authors': 'Marx, Engels',
            'isbn': 1234,
            'description': 'Manifesto comunista description',
            'url': '#result-0',
            'ranking': 0
        }
    ],
    "text_results": []
}

@app.route('/', methods=['GET'])
def home():
    return render_template(os.path.join('home.html'), field_results=results['field_results'], text_results=results['text_results'], required_field=False)

@app.route('/search/text/', methods=['POST'])
def text_search():
    content = request.form['content']
    if not content:
        return render_template(os.path.join('home.html'), text_results=results['text_results'], required_field=True)
    else:
        # call function here to generate ranking and return an array of responses
        results['field_results'] = []
        results['text_results'] = []
        len_res = len(results['text_results'])
        results['text_results'].append({
            'content': content,
            'url': f"#result-{len_res}",
            'ranking': len_res
        })
        return redirect(url_for('home'))

@app.route('/search/field/', methods=['POST'])
def field_search():
    title = request.form['title']
    publisher = request.form['publisher']
    authors = request.form['authors']
    isbn = request.form['isbn']
    description = request.form['description']

    if not (title or publisher or authors or isbn or description):
        return render_template(os.path.join('home.html'), field_results=results['field_results'], required_field=True)
    else:
        # call function here to generate ranking and return an array of responses
        print(field_query(request.form))
        results['text_results'] = []
        results['field_results'] = []
        len_res = len(results['field_results'])
        results['field_results'].append({
            'title': title,
            'publisher': publisher,
            'authors': authors,
            'isbn': isbn,
            'description': description,
            'url': f"#result-{len_res}",
            'ranking': len_res
        })
        return redirect(url_for('home'))

if __name__ == '__main__':
   app.run(host='127.0.0.1',port=5000,debug=True)