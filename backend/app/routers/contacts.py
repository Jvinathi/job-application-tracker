from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.contact import Contact
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/contacts", tags=["Contacts"])
security = HTTPBearer()

class ContactCreate(BaseModel):
    name: str
    role: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    company: Optional[str] = None

class ContactResponse(BaseModel):
    id: int
    name: str
    role: Optional[str]
    email: Optional[str]
    linkedin_url: Optional[str]
    company: Optional[str]

    class Config:
        from_attributes = True

def get_current_user_dep(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(credentials.credentials, db)

@router.get("/", response_model=List[ContactResponse])
def get_contacts(current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    return db.query(Contact).filter(Contact.user_id == current_user.id).all()

@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(data: ContactCreate, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    contact = Contact(**data.dict(), user_id=current_user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact