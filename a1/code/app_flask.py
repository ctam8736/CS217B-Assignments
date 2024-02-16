"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""


from flask import Flask, request, render_template

from spacy_docs import SpacyDocument

app = Flask(__name__)


# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt', encoding='utf-8').read())
    else:
        text = request.form['text']
        doc = SpacyDocument(text)
        ner_markup = doc.get_entities_with_markup()
        dep_markup = doc.get_dependencies_with_markup()
        markup = (ner_markup + dep_markup).strip("</markup><markup>")
        print(markup)
        markup_paragraphed = ''
        for line in markup.split('\n'):
            if line.strip() == '':
                markup_paragraphed += '<p/>\n'
            else:
                markup_paragraphed += line
        return render_template('result.html', markup=markup_paragraphed)

# alternative where we use two resources

@app.get('/get')
def index_get():
    return render_template('form2.html', input=open('input.txt').read())

@app.post('/post')
def index_post():
    text = request.form['text']
    doc = SpacyDocument(text)
    markup = doc.get_entities_with_markup()
    markup_paragraphed = ''
    for line in markup.split('\n'):
        if line.strip() == '':
            markup_paragraphed += '<p/>\n'
        else:
            markup_paragraphed += line
    return render_template('result2.html', markup=markup_paragraphed)


if __name__ == '__main__':

    app.run(debug=True)
