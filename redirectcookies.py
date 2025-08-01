from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse

app = FastAPI()

# Simulated token
VALID_TOKEN ="open"

@app.get("/")
async def root(request: Request):
    token = request.cookies.get("mytoken")
    if token == VALID_TOKEN:
        return RedirectResponse(url="/see")
    else:
        return RedirectResponse(url="/login")

@app.get("/see")
async def see_page():
    return {"message": "📝 Welcome to the secret diary!"}

@app.get("/login")
async def login_page():
    return {"message": "🔒 Please log in to see the secret diary."}

@app.get("/set-token")
async def set_token():
    response = RedirectResponse(url="/")
    response.set_cookie(key="mytoken", value=VALID_TOKEN)
    return response
