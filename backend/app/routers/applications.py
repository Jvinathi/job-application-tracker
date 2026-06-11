from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse, StatusUpdate
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])
security = HTTPBearer()

def get_current_user_dep(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(credentials.credentials, db)

@router.get("/", response_model=List[ApplicationResponse])
def get_applications(current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    return db.query(Application).filter(Application.user_id == current_user.id).order_by(Application.kanban_order).all()

@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(data: ApplicationCreate, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    app_obj = Application(**data.dict(), user_id=current_user.id)
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj

@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    app_obj = db.query(Application).filter(Application.id == app_id, Application.user_id == current_user.id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj

@router.put("/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, data: ApplicationUpdate, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    app_obj = db.query(Application).filter(Application.id == app_id, Application.user_id == current_user.id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(app_obj, field, value)
    db.commit()
    db.refresh(app_obj)
    return app_obj

@router.patch("/{app_id}/status", response_model=ApplicationResponse)
def update_status(app_id: int, data: StatusUpdate, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    app_obj = db.query(Application).filter(Application.id == app_id, Application.user_id == current_user.id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    app_obj.status = data.status
    if data.kanban_order is not None:
        app_obj.kanban_order = data.kanban_order
    db.commit()
    db.refresh(app_obj)
    return app_obj

@router.delete("/{app_id}", status_code=204)
def delete_application(app_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    app_obj = db.query(Application).filter(Application.id == app_id, Application.user_id == current_user.id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app_obj)
    db.commit()