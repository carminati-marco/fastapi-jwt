from fastapi import FastAPI

app = FastAPI()
from fastapi import Depends
from auth.utils import *

SKILLS = [
    {"user": "johndoe",  "name": "super power"},
    {"user": "johndoe",  "name": "fire"},
    {"user": "NOTjohndoe",  "name": "water"},
]


@app.get("/")
def read_root():
    return {"Hello": "MS SKILLS"}


@app.get("/skills")
def read_skills(token: str = Depends(oauth2_scheme)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user = payload.get("sub")
    skills = [s.get("name") for s in SKILLS if s.get("user") == user]
    return {"skills": skills, "payload": payload}