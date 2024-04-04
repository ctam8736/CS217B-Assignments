"""Simple Web interface to spaCy entity recognition

python app_flask.py
To see the pages point your browser at http://127.0.0.1:5000.

TODO: upon form submission, push entities and relations to a database
create a button to navigate to database display, and then back again

"""


from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from spacy_docs import SpacyDocument
from tabulate import tabulate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spacy.db'
db = SQLAlchemy(app)


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120))
    label = db.Column(db.String(120))

    def __repr__(self):
        return '<Entity %r %r>' % (self.text, self.label)


class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(120))
    dep = db.Column(db.String(120))
    text = db.Column(db.String(120))

    def __repr__(self):
        return '<Relation %r %r %r>' % (self.head, self.dep, self.text)


with app.app_context():
    db.create_all()


def push_entities_to_database(doc):
    entities = doc.get_entities()
    with app.app_context():
        for e in entities:
            db.session.add(Entity(text=e[3], label=e[2]))
        db.session.commit()


def push_dependencies_to_database(doc):
    dependencies = doc.get_dependencies()
    with app.app_context():
        for dep in dependencies:
            db.session.add(Relation(head=dep[0], dep=dep[1], text=dep[2]))
        db.session.commit()


# Serve HTML for website


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt', encoding='utf-8').read())
    else:
        text = request.form['text']
        doc = SpacyDocument(text)
        push_entities_to_database(doc)
        push_dependencies_to_database(doc)
        ner_markup = doc.get_entities_with_markup()
        dep_markup = doc.get_dependencies_with_markup()
        markup = (ner_markup + dep_markup).strip("</markup><markup>")
        markup_paragraphed = ''
        for line in markup.split('\n'):
            if line.strip() == '':
                markup_paragraphed += '<p/>\n'
            else:
                markup_paragraphed += line
        return render_template('result.html', markup=markup_paragraphed)


@app.route('/database', methods=['GET'])
def database_get():
    if request.method == 'GET':
        markup = ""
        with app.app_context():
            entities = Entity.query.all()
            data = [['Text', 'Label']]
            data.extend([[e.text, e.label] for e in entities])
            markup += 'Entities'
            markup += tabulate(data, tablefmt='html')

            data = [['Entity', 'Count', 'Head', 'Dependency Type', "Text"]]
            for e in entities:
                dep_query = Relation.query.filter_by(head=e.text)
                data.extend([[e, dep_query.count(), d.head, d.dep, d.text] for d in dep_query])
            markup += 'Relations with Entities'
            markup += tabulate(data, tablefmt='html')
        return render_template('database.html', markup=markup)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
