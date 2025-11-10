curl "http://127.0.0.1:5005/data"
curl "http://127.0.0.1:5005/data" -H "Content-Type: application/json" -d '{"text": "data 01"}'
curl -X DELETE "http://127.0.0.1:5005/data" -H "Content-Type: application/json" -d '{"id": "0"}'

