from fastapi.responses import Response,JSONResponse
from fastapi import FastAPI,Request

app=FastAPI()


@app.middleware("http")
async def block_header(request:Request,call_next):
    auth_header=request.headers.get("auth-token")
    
    if auth_header!="suhar":
        return JSONResponse(content={"detial":"unathorized you shall not pass"})
    
    
    response=await call_next(request)
    response.headers["Naam"]="suhar"
    return response

@app.get("/")
async def home():
    return {"welcome home"}