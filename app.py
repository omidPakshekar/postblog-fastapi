import fastapi
from fastapi import security, Depends
from sqlalchemy import orm 
from schemas import *
from services import *
from typing import List
import services

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


@app.post('/login')
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


@app.post('/api/v1/posts', response_model=PostResponse)
async def create_post(post_request: PostRequest, user: UserRequest = fastapi.Depends(current_user),
                    db: orm.Session = fastapi.Depends(get_db)):

    return await services_create_post(user=user, db=db, post=post_request)


@app.get(base_addr + '/posts/user', response_model=List[PostResponse])
async def get_posts_by_user(user: UserRequest = fastapi.Depends(current_user),
    db: orm.Session = fastapi.Depends(get_db)):
    return await services.get_posts_by_user(user=user, db=db)

@app.get(base_addr + 'posts/{post_id}/', response_model=PostResponse)
async def get_post_detail(post_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    post = await services.get_post_detail(post_id=post_id, db=db)
    return post




