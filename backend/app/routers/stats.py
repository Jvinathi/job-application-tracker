from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.application import Application
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/stats", tags=["Stats"])
security = HTTPBearer()

def get_current_user_dep(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(credentials.credentials, db)

@router.get("/")
def get_stats(current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    user_id = current_user.id
    total = db.query(Application).filter(Application.user_id == user_id).count()

    by_status = db.query(Application.status, func.count(Application.id)).filter(
        Application.user_id == user_id
    ).group_by(Application.status).all()

    status_map = {s: c for s, c in by_status}
    applied = status_map.get("applied", 0)
    shortlisted = status_map.get("shortlisted", 0)
    interview = status_map.get("interview", 0)
    offer = status_map.get("offer", 0)
    rejected = status_map.get("rejected", 0)

    got_response = shortlisted + interview + offer + rejected
    response_rate = round((got_response / total * 100), 1) if total > 0 else 0
    offer_rate = round((offer / total * 100), 1) if total > 0 else 0

    by_platform = db.query(Application.platform, func.count(Application.id)).filter(
        Application.user_id == user_id,
        Application.platform != None
    ).group_by(Application.platform).all()

    return {
        "total": total,
        "applied": applied,
        "shortlisted": shortlisted,
        "interview": interview,
        "offer": offer,
        "rejected": rejected,
        "response_rate": response_rate,
        "offer_rate": offer_rate,
        "by_platform": [{"platform": p, "count": c} for p, c in by_platform]
    }