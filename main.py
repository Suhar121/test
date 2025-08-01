from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/secret")
def get_secret(authorization: str = Header(None)):
    if authorization == "Suhar":
        return {"message": "You have access!"}
    return {"error": "You shall not pass! ⚔️"}