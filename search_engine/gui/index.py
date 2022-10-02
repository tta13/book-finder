import os
from flask import Flask, render_template, request, url_for, redirect
from controller import *

app = Flask(__name__)

results = {
    "field_results": [
        {
            'title': 'Manifesto comunista',
            'publisher': 'Boitempo',
            'authors': ['Marx', 'Engels'],
            'isbn': 1234,
            'description': 'Manifesto comunista description',
            'url': '#result-0',
        }
    ],
    "text_results": []
}

query = {
    "current": []
}

@app.route('/', methods=['GET'])
def home():
    return render_template(os.path.join('home.html'), field_results=results['field_results'], text_results=results['text_results'], required_field=False, current_query=query['current'])

@app.route('/search/text/', methods=['POST'])
def text_search():
    content = request.form['content']
    if not content:
        return render_template(os.path.join('home.html'), text_results=results['text_results'], required_field=True, current_query=False)
    else:
        # call function here to generate ranking and return an array of responses
        results['text_results'] = text_query(content)
        query['current'] = [i for i in [content] if i]
        results['field_results'] = []
        return redirect(url_for('home'))

@app.route('/search/field/', methods=['POST'])
def field_search():
    title = request.form['title']
    publisher = request.form['publisher']
    authors = request.form['authors']
    isbn = request.form['isbn']
    description = request.form['description']
    # Check if some field is filled
    if not (title or publisher or authors or isbn or description):
        return render_template(os.path.join('home.html'), field_results=results['field_results'], required_field=True, current_query=False)
    else:
        # Submit query and receive results
        results['field_results'] = field_query(request.form)
        query['current'] = [i for i in [title, publisher, authors, isbn, description] if i]
        results['text_results'] = []
        return redirect(url_for('home'))

if __name__ == '__main__':
   app.run(host='127.0.0.1',port=5000,debug=True)