from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.user import User
from app.schemas.auth import UserLogin
from app.utils.hashing import pwd_context
from app.utils.token import create_access_token

router = APIRouter()

@router.post("/login")
def user_login(login_data: UserLogin, db: Session = Depends(get_db)):
    # Fetch user from DB
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not pwd_context.verify(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate token
    token = create_access_token({"sub": user.email, "role": user.role})

    return {"access_token": token, "token_type": "bearer"}
