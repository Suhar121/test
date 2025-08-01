from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, PlainTextResponse

app = FastAPI()

ALLOWED_HOSTS = ["vip.example.com", "localhost"]

@app.middleware("http")
async def check_host_and_redirect(request: Request, call_next):
    host = request.headers.get("host", "")
    print(f"🤔 Someone's knocking... Host: {host}")

    if any(allowed in host for allowed in ALLOWED_HOSTS):
        if request.url.path == "/":
            print("✅ VIP spotted! Redirecting to /see")
            return RedirectResponse(url="/see")
    
    # Proceed normally if not redirected
    return await call_next(request)



@app.get("/")
async def main():
    return PlainTextResponse("🏠 Welcome to the boring main page!")

@app.get("/see")
async def see():
    return PlainTextResponse("🎉 VIP lounge! You've made it.")
