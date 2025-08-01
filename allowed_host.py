from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 👇 Your whitelist of allowed hostnames
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "streamlit.com"]

@app.middleware("http")
async def validate_host(request: Request, call_next):
    host = request.headers.get("host", "").split(":")[0]  # Remove port if any
    if host not in ALLOWED_HOSTS:
        return JSONResponse(status_code=403, content={"detail": "Host not allowed"})
    return await call_next(request)

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI app!"}