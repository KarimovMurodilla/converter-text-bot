from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import update, delete
from sqlalchemy.orm import sessionmaker

from utils.db_api.base import Base
from utils.db_api.models import Users

db_string = r"sqlite:///database.db"
db = create_engine(db_string)  

Session = sessionmaker(db)  
session = Session()

Base.metadata.create_all(db)


class Database:
    # ---Users---
    def reg_user(self, user_id: str, username: str, lang: str):
        """Some docs"""
        session.merge(
            Users(
                user_id = user_id, 
                username = username,
                lang = lang
            )
        )
        session.commit()
    

    def get_user(self, user_id) -> Users:
        """Some docs"""
        response = session.query(Users).filter(Users.user_id == user_id).first()
        return response

    
    def update_lang(self, user_id, lang):
        """Some docs"""
        session.execute(
                update(Users).filter(Users.user_id == user_id).
                values(lang = lang)
        )
        session.commit()