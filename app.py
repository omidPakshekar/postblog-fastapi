import fastapi
from fastapi import security
from sqlalchemy import orm 
from schemas import *
from services import *

app = fastapi.FastAPI()


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
