from app.main import handler

# Simulated API Gateway HTTP API v2 event
event = {
    "version": "2.0",
    "routeKey": "GET /api/orders/ping",
    "rawPath": "/api/orders/ping",
    "rawQueryString": "",
    "headers": {
        "host": "localhost",
        "x-forwarded-proto": "http"
    },
    "requestContext": {
        "http": {
            "method": "GET",
            "path": "/api/orders/ping",
            "sourceIp": "127.0.0.1",
            "userAgent": "curl/7.88.1"
        }
    },
    "isBase64Encoded": False
}


response = handler(event, {})
print(response)
