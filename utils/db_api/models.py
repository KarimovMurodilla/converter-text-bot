from datetime import datetime
from distutils.sysconfig import get_makefile_filename
from sqlalchemy import Column, BigInteger, String, Integer, DateTime

from utils.db_api.base import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))


class Audio(Base):
    __tablename__ = "audio"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    file_id = Column(String(50))
    file_path = Column(String(50))


class Document(Base):
    __tablename__ = "document"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    file_id = Column(String(50))
    file_path = Column(String(50))
    text = Column(String)
    date = Column(DateTime, default = datetime.utcnow)