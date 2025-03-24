from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from model import GoogleUser
from model import RoleTable

role_types = ["account", "manager"]

db_dependencies = Annotated[Session, Depends(get_db)]


router = APIRouter()


@router.get("/Get_ALL_USER_DATA")
async def get(db: db_dependencies):
    users = db.query(GoogleUser).all()

    return users


@router.put("/give_role/")
async def give_role(db: db_dependencies, email: str, role_type: str):

    role = db.query(RoleTable).filter(RoleTable.email == email).first()
    if not role:
        raise HTTPException(status_code=401, detail="Email not found")
    
    if role_type not in role_types:
        raise HTTPException(status_code=404, detail="This role not avaiable only manager and accountatn is abaiable")
    
    role.role = role_type

    db.add(role)
    db.commit()

    return "Role has been successfully assigned"






