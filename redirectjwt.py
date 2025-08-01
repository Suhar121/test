from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "open"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class AuthRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/":
            auth_header = request.headers.get("Authorization")

            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    # Token is valid, redirect to /see
                    return RedirectResponse(url="/see")
                except JWTError:
                    pass  # Invalid token, fall through to redirect to /login
            
            return RedirectResponse(url="/login")

        return await call_next(request)


app.add_middleware(AuthRedirectMiddleware)

@app.post("/login")
async def login():
    # Imagine credentials checked (e.g., username/password)
    user_data = {"sub": "suhar_the_legend"}
    token = create_access_token(user_data)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/see")
async def see_page():
    return {"message": "📖 Welcome to the secret diary!"}


