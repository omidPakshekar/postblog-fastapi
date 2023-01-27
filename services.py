import database
import models
import email_validator
import fastapi 
from sqlalchemy import orm  
from schemas import *  
from passlib import hash
import jwt 

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

