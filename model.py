from database import Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum, Text
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, Enum("admin", "viewer", "manager", name="role_table"), default="viewer")
    acc_created = Column(String, default=datetime.utcnow)

    document = relationship("Document", back_populates="user")



class Document(Base):

    __tablename__ = "document"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    document_url = Column(String)
    document_name = Column(String)
    document_type = Column(String)

    upload_at = Column(Date, default=datetime.utcnow)


    user = relationship("User", back_populates="document")


class OCRresult(Base):

    __tablename__ = "ocr_result"

    id = Column(Integer, primary_key=True, index=True)
    
    text = Column(Text)
    date = Column(Date, default=datetime.utcnow)
    document_id = Column(Integer, ForeignKey("document.id"))



class GoogleUser(Base):

    __tablename__ = "google_user"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String)
    username = Column(String)
    user_email = Column(String)
    first_logged_in = Column(Date)
    last_accessed = Column(Date)
    user_pic = Column(String)



class GoogleToken(Base):
 
    __tablename__ = "google_token"
    id = Column(Integer, primary_key=True, index=True)

    access_token = Column(String)
    user_email = Column(String)
    session_id = Column(String)


class RoleTable(Base):

    __tablename__="role_table"


    id = Column(Integer, primary_key=True, index=True)

    email=Column(String)
    role=Column(String)


class Log(Base):

    __tablename__="log_table"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("google_user.id"))
    email = Column(Integer, ForeignKey("google_user.user_email"))

    activity = Column(String)
    documnent_id = Column(Integer, ForeignKey("document.id"))
    date = Column(Date, default=datetime.utcnow)













