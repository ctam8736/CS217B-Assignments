Using Python 3.10.4 and Docker Desktop.

### FastAPI

```
cd assignment3\FastAPI
docker build -t fastapi-nlp .  
docker compose up --build
```

Navigate to localhost:8500.

Test the API with the following commands to the /dep and /ner routes. Ensure input.json has the correct content.

```bash
$ curl http:/127.0.0.1:8000
$ curl -X POST -H "Content-Type: application/json" --data-binary "@input.json" http://127.0.0.1:8500/dep
```

### Streamlit

```
cd assignment3\Streamlit
docker build -t streamlit-nlp .
docker compose up --build
```

Navigate to localhost:8501.

### Flask

```
cd assignment3\Flask
docker build -t flask-nlp .
docker compose up --build
```

Navigate to localhost:5000, see database functionality at bottom of processing page.
