from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    print(f"⬅️ Incoming request: {request.method} {request.url}")

    # Process request (go to the actual route)
    response = await call_next(request)

    process_time = time.time() - start_time
    print(f"➡️ Completed in {process_time:.4f}s")

    return response

@app.get("/")
def read_root():
    return {"message": "Hello World"}