import datetime
import sqlalchemy
from sqlalchemy import orm 
from passlib import hash 
import database




class UesrModel(database.Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow())
    posts = orm.relationship('PostModel', back_populates="users")

    def password_verification(self, password: str):
       return hash.bcrypt.verify(password, self.password_hash)

class PostModel(database.Base):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    post_title = sqlalchemy.Column(sqlalchemy.String, index=True)
    post_image = sqlalchemy.Column(sqlalchemy.String)
    post_description = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow())
    users = orm.relationship('UesrModel', back_populates="posts")


