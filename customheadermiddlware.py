from fastapi.responses import Response
from fastapi import FastAPI,Request
app=FastAPI()

@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Developer"] = "Suhar the Wizard"
    return response