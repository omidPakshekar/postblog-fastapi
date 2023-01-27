import fastapi
from fastapi import security, Depends
from sqlalchemy import orm 
from schemas import *
from services import *


app = fastapi.FastAPI()


APP_SECRET_CODE = "SECRET"
base_addr = '/api/v1/'

@app.post(base_addr + '/users')
async def register_user(user: UserRequest, db: orm.Session = fastapi.Depends(get_db)):
    # call to check if user with email exist 
    db_user = await get_user_by_email(email=user.email, db=db)
    # if user found throw execption
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="email allready exist")
    
    # create user and return token
    user = await create_user(user=user, db=db)
    print('uuuser', user)
    return await create_token(user=user)


@app.post(base_addr + '/login')
async def login_user(form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
                 db: orm.Session = fastapi.Depends(get_db)):
    
    db_user = await login(email=form_data.username, password=form_data.password, db=db)
    # invalid login throw exception
    if not db_user:
        raise fastapi.HTTPException(status_code=401, detail='wrong logn credintial')
    return await create_token(db_user)


@app.get(base_addr + '/users/current-user', response_model=UserResponse)
async def get_current_user(user: UserResponse = Depends(current_user)):
    return user
