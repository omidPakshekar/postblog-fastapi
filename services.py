import database
import models
import email_validator
import fastapi 
import jwt 
from fastapi import security, Depends
from sqlalchemy import orm  
from schemas import *  
from passlib import hash
from models import *

APP_SECRET_CODE = "SECRET"
base_addr = '/api/v1/'
oauth2scheams = security.OAuth2PasswordBearer(base_addr + 'login')


def create_db():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db 
    finally:
        db.close()

# create_db()

async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.UesrModel).filter(models.UesrModel.email == email).first()


async def create_user(user: UserRequest, db: orm.Session):
    # check for valid email 
    try:
        isValid = email_validator.validate_email(email=user.email)
        email = isValid.email 
    except email_validator.EmailNotValidError:
        raise fastapi.HTTPException(status_code=400, detail="Provide valid email")

    hashed_password = hash.bcrypt.hash(user.password)

    user_obj = models.UesrModel(
        email=email,
        name=user.name,
        password_hash=hashed_password
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: models.UesrModel):
    # convert user modle to user schema
    user_schema =  UserResponse.from_orm(user)
    # convert obj to dic
    print('schema', user_schema, 'endschema')
    user_dict = user_schema.dict()
    del user_dict['created_at']
    token = jwt.encode(user_dict, 'SECRET')

    return dict(access_token=token, token_type='bearer')

async def login(email: str, password: str, db: orm.Session):
    db_user = await get_user_by_email(email=email, db=db)
    if not db_user:
        return False 
    if not db_user.password_verification(password=password):
        return False 
    return db_user


async def current_user(db: orm.Session = Depends(get_db), token: str = Depends(oauth2scheams)):
    
    try:
        payload = jwt.decode(token, APP_SECRET_CODE, algorithms=['HS256'])
        # get user by id and (email, name)
        db_user = db.query(UesrModel).get(payload['id'])
    except:
        raise fastapi.HTTPException(status_code=401, detail='wrong Credentials')
    return UserResponse.from_orm(db_user)











