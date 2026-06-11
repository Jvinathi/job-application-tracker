from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

def get_db_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(credentials.credentials, db)

@router.post("/register", response_model=Token, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email already registered
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "created_at": new_user.created_at
    }
    }

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at
    }
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_db_user)):
    return current_user