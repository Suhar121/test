from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

# =================== SETTINGS ===================
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# =================== FAKE USER DB ===================
fake_users_db = {}

# =================== JWT TOKEN ===================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =================== GET CURRENT USER ===================
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid user")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# =================== SIGNUP ===================
@app.post("/signup")
def signup(form: OAuth2PasswordRequestForm = Depends()):
    if form.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[form.username] = {
        "username": form.username,
        "password": form.password  # (Hashing is skipped for simplicity)
    }
    return {"msg": "User created"}

# =================== LOGIN ===================
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form.username)
    if not user or user["password"] != form.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}

# =================== PROTECTED ROUTE ===================
@app.post("/create")
def create_secret_data(user: str = Depends(get_current_user)):
    return {"msg": f"🧙 {user} created something magical!"}
