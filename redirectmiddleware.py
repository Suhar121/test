from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

VALID_TOKEN = "open"

# 🧙 Our custom middleware
class AuthRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 🕵️ Only intercept the root path
        if request.url.path == "/":
            token = request.cookies.get("my_token")
            
            if token == VALID_TOKEN:
                # 🟢 Has token → go to secret diary
                return RedirectResponse(url="/see")
            else:
                # 🔒 No token → go login
                return RedirectResponse(url="/login")
        
        # Let everything else pass through untouched 🛣️
        response = await call_next(request)
        return response

# Add middleware to FastAPI
app.add_middleware(AuthRedirectMiddleware)


@app.get("/see")
async def see_page():
    return {"message": "📝 Welcome to the secret diary!"}

@app.get("/login")
async def login_page():
    return {"message": "🔒 Please log in to see the secret diary."}

@app.get("/set-token")
async def set_token():
    response = RedirectResponse(url="/")
    response.set_cookie(key="my_token", value=VALID_TOKEN)
    return response
