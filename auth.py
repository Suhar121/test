from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

app = FastAPI()

# Pretend database
fake_users_db = {
    "suhar": {"username": "suhar", "password": "kashmir123", "role": "admin"},
    "ali": {"username": "ali", "password": "guest123", "role": "guest"}
}

# For simplicity, we'll use this token manually
fake_token_db = {
    "suhar-token": "suhar",
    "ali-token": "ali"
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 1️⃣ Login route
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = fake_users_db.get(username)
    if user and user["password"] == password:
        # Normally here you'd return a JWT
        return {"access_token": f"{username}-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# 2️⃣ Dependency to check token
def get_current_user(token: str = Depends(oauth2_scheme)):
    if token not in fake_token_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = fake_token_db[token]
    return fake_users_db[username]

# 3️⃣ Protected route
@app.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['username']}! You are an {user['role']}."}