from fastapi import FastAPI

app = FastAPI()
from ms_auth.routers import auth


app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "MS AUTH"}



