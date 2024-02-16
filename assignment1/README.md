Python version: 3.10

No additional dependencies.
(From outer README):
```bash
$ pip install jupyter
$ pip install spacy
$ python -m spacy download en_core_web_sm
$ pip install flask flask-restful flask-sqlalchemy
$ pip install streamlit graphviz
$ pip install mypy
```

FastAPI:

```bash
uvicorn app_fastapi:app --reload
curl -X POST -H "Content-Type: application/json" --data-binary "@input.json" http://127.0.0.1:8000/dep
```

Flask:

```bash
python app_flask.py
```

(then go to http://127.0.0.1:5000)

Streamlit:

```bash
streamlit run app_streamlit.py
```
