# example curl commands for testing
# get curls
curl "http://127.0.0.1:5005/data"

# post curls
curl "http://127.0.0.1:5005/data" -H "Content-Type: application/json" -d '{"text": "data 01"}'

# put curls
curl "http://127.0.0.1:5005/imagedata" -T test_image.png -H "Content-Type: image/png"

# delete curls
curl -X DELETE "http://127.0.0.1:5005/data" -H "Content-Type: application/json" -d '{"id": "0"}'
