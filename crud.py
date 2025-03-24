from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query, Cookie, Request
from starlette import status
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .minio_uplode import uplode_file
from model import Document, OCRresult, RoleTable, Log
from .auth import get_current_user
import pytesseract
from PIL import Image
from io import BytesIO
from collections import Counter
from .celery import extract_text
from sqlalchemy import func
import base64

import spacy
nlp = spacy.load("en_core_web_sm")


router = APIRouter()

db_dependiencies = Annotated[Session, Depends(get_db)]

user_dependiencies = Annotated[dict, Depends(get_current_user)]


def get_role(db: Session, user: dict):

    email = user.get("email")

    role = db.query(RoleTable).filter(RoleTable.email == email).first()

    if not role:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return role.role



@router.get("/searech_file/")
async def search(db: db_dependiencies, current_user: user_dependiencies, Search: str = Query(...)):

    role = get_role(current_user)
    search_query = func.plainto_tsquery('english', search)


    if role == "manager":

        document = db.query(OCRresult).filter(func.to_tsvector('english', OCRresult.text).op("@@")(search_query)).all()
        return document
    
    if role == "account":

        document = db.query(Document).filter(Document.user_id == current_user.get("user_id")).filter(func.to_tsvector('english', OCRresult.text).op("@@")(search_query)).all()
        return document



@router.get("/get_files")
async def get_files(db: db_dependiencies, current_user: user_dependiencies):
    role = get_role(user=current_user, db=db)

    if role == "manager":

        document = db.query(Document).all()
        return document
    
    if role == "account":

        document = db.query(Document).filter(Document.user_id == current_user.get("user_id"))
        return document



@router.post("/Uplode_Document/", status_code=status.HTTP_201_CREATED)
async def uplode_document(user: user_dependiencies, db: db_dependiencies, file: UploadFile = File(...)):


    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    role = get_role(user=user, db=db)

    if role not in ["account", "manager"]:
        raise HTTPException(status_code=401, detail="unauthorized")
    

    file_bytes = await file.read()  # read the content
    encoded_file = base64.b64encode(file_bytes).decode('utf-8')  # encode bytes to string
    text = extract_text.delay(encoded_file, file.filename)  # pass encoded string and filename
    data = await uplode_file(file=file)

    
    uplode = Document(
        document_url=data["url"],
        document_name=data["document_name"],
        document_type=data["document_type"],
        user_id=user.get("user_id")
    )


    db.add(uplode)
    db.commit()

    uplode_ocr = OCRresult(
        text=text,
        document_id=uplode.id
    )

    db.add(uplode_ocr)
    db.commit()

    log = Log(
        user_id=user.get("user_id"),
        email=user.get("email"),
        activity="uplode",
        document_id=uplode.id
    )

    db.add(log)
    db.commit()

    return "Document has been successfully added"

@router.delete("/Delete_Document/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(current_user: user_dependiencies, db: db_dependiencies, file_id: int = Query(gt=0)):
    role = get_role(user=current_user, db=db)

    if role == "manager":

        file = db.query(Document).filter(Document.id == file_id).first()

        if not file:
            raise HTTPException(status_code=404, detail="File with this id not found")
        
        db.delete(file)
        db.commit()

        log = Log(
        user_id=current_user.get("user_id"),
        email=current_user.get("email"),
        document_id=file.id,
        activity="deleted"
    )

        db.add(log)
        db.commit()

        db.delete(file)
        db.commit()

        return "Document successfully deleted"
    

    
    raise HTTPException(status_code=401, detail="Unauthorized")



