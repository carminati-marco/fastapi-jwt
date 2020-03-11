import json

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from urllib.request import Request, urlopen

from auth.models import Token
from auth.utils import *

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "email": user.email, "extra_info": "some extra info"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(token: str = Depends(oauth2_scheme)):

    u = await get_current_user(token=token)
    hed = {'Authorization': 'Bearer ' + token}
    current_user = await get_current_active_user(u)

    # calls another webservice using the token.
    req = Request("http://localhost:8001/skills", headers=hed)
    with urlopen(req) as response:
        r = json.loads(response.read().decode("utf-8"))

    return [{"item_id": "Foo", "owner": current_user.username, "main_skill": r}]