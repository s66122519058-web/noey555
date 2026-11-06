# Zoo Visitors Report API

FastAPI reads the Data.go.th January 2569 CSV beside `main.py` and returns its real rows as JSON. The source file contains 63 data records.

## Run (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8002
```

Visit `http://127.0.0.1:8002/docs` and execute `GET /api/zoo-visitors`. The API response includes dataset provenance, fiscal year, record count, and rows read from the CSV.

## Postman

Import `postman_collection.json` and send the request. Its base URL is set to `http://127.0.0.1:8002`.

Source dataset: https://data.go.th/dataset/zoo-visitors2569
