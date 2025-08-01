from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI()

# In-memory store: {ip: [timestamp1, timestamp2, ...]}
request_log = {}

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    window_seconds = 30
    max_requests = 3

    # Initialize if first time
    if client_ip not in request_log:
        request_log[client_ip] = []

    # Filter timestamps in the current time window
    request_log[client_ip] = [
        timestamp for timestamp in request_log[client_ip] if now - timestamp < window_seconds
    ]

    if len(request_log[client_ip]) >= max_requests:
        return JSONResponse(
            content={"detail": "⛔ Rate limit exceeded. Try again later."},
            status_code=429
        )

    request_log[client_ip].append(now)
    return await call_next(request)

@app.get("/magic")
async def magic_endpoint():
    return {"message": "✨ Welcome to the secret endpoint!"}
